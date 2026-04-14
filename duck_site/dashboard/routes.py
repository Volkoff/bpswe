from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
import shutil
from models import db, Domain, Database, User
from sqlalchemy import text

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    user_id = session["user_id"]
    user = User.query.get(user_id)
    
    if request.method == "POST":
        domain_name = request.form.get("domain_name")
        if domain_name:
            # Basic validation
            existing = Domain.query.filter_by(domain_name=domain_name).first()
            if existing:
                flash("Domain already exists!")
            else:
                doc_root = f"{user.home_directory}/{domain_name}"
                
                # Automatically create directory structure if it doesn't exist
                os.makedirs(doc_root, exist_ok=True)
                
                # Ensure the FTP user (UID 1000) owns the new directory
                try:
                    shutil.chown(user.home_directory, user=1000, group=1000)
                    shutil.chown(doc_root, user=1000, group=1000)
                except Exception as e:
                    print(f"Chown failed for {doc_root}: {e}")
                
                # Add a default welcome page
                index_path = os.path.join(doc_root, "index.html")
                if not os.path.exists(index_path):
                    with open(index_path, "w") as f:
                        f.write(f"<h1>Welcome to {domain_name}!</h1><p>Your server is ready.</p>")
                    
                    # Ensure index.html is also owned by the FTP user
                    try:
                        shutil.chown(index_path, user=1000, group=1000)
                    except Exception as e:
                        print(f"Chown failed for {index_path}: {e}")

                new_domain = Domain(domain_name=domain_name, document_root=doc_root, active=True, user_id=user_id)
                db.session.add(new_domain)
                db.session.commit()
                flash("New server deployed successfully!")
        return redirect(url_for("dashboard.dashboard"))

    # Test DB Connection with raw SQL select
    try:
        result = db.session.execute(text("SELECT version();")).fetchone()
        db_version = result[0] if result else "Unknown"
    except Exception as e:
        db_version = f"Error: {str(e)}"

    try:
        domains = Domain.query.filter_by(user_id=user_id).all()
    except Exception as e:
        domains = []
        print("Domain query failed:", e)

    try:
        databases = Database.query.filter_by(user_id=user_id).all()
    except Exception as e:
        databases = []
        print("Database query failed:", e)

    return render_template("dashboard/dashboard.html", domains=domains, databases=databases, db_version=db_version)

@dashboard_bp.route("/dashboard/<int:service_id>", methods=["GET", "POST"])
def individual_dashboard(service_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    domain = Domain.query.get_or_404(service_id)
    
    # Ensure the domain belongs to the logged in user
    if domain.user_id != session["user_id"]:
        flash("Unauthorized access!")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "toggle_status":
            old_root = domain.document_root
            if domain.active:
                # Disabling: rename folder and update root
                new_root = old_root.rstrip('/') + "_disabled"
                try:
                    if os.path.exists(old_root):
                        os.rename(old_root, new_root)
                        domain.document_root = new_root
                        domain.active = False
                    else:
                        flash("Warning: Document root directory not found, status updated only in database.")
                        domain.active = False
                except Exception as e:
                    flash(f"Error disabling domain: {str(e)}")
            else:
                # Enabling: remove _disabled from folder name
                if old_root.endswith("_disabled"):
                    new_root = old_root[:-9]  # removes "_disabled"
                    try:
                        if os.path.exists(old_root):
                            if os.path.exists(new_root):
                                flash("Error: Target directory already exists. Cannot enable domain.")
                            else:
                                os.rename(old_root, new_root)
                                domain.document_root = new_root
                                domain.active = True
                        else:
                            flash("Warning: Disabled directory not found, status updated only in database.")
                            domain.active = True
                    except Exception as e:
                        flash(f"Error enabling domain: {str(e)}")
                else:
                    # Root doesn't end in _disabled, just activate
                    domain.active = True

            db.session.commit()
            status_text = "stopped" if not domain.active else "started"
            flash(f"Domain {domain.domain_name} has been {status_text}.")
            return redirect(url_for('dashboard.individual_dashboard', service_id=domain.domain_id))
        elif action == "destroy_server":
            domain_name = domain.domain_name
            try:
                shutil.rmtree(domain.document_root)
            except Exception as e:
                print(f"Failed to remove directory {domain.document_root}: {e}")
            db.session.delete(domain)
            db.session.commit()
            flash(f"Server {domain_name} has been destroyed.")
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('dashboard.individual_dashboard', service_id=domain.domain_id))
        
    return render_template("dashboard/individual.html", domain=domain)
