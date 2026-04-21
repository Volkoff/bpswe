from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
import os
import shutil
import re
import urllib.parse

from sqlalchemy import text, create_engine
from models import db, Domain, Database, User

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")


def get_base_name(value: str) -> str:
    base = value.split("@")[0].split(".")[0].lower()
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = base.strip("_")

    if not base:
        base = "user"

    return base


def make_safe_db_name(domain_name: str) -> str:
    base = get_base_name(domain_name)
    return f"{base}_db"[:30]


def make_safe_db_user(domain_name: str) -> str:
    base = get_base_name(domain_name)
    return f"{base}_user"[:32]


def make_db_password(username: str) -> str:
    base = get_base_name(username)
    return f"{base}_password"


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    user = User.query.get(user_id)

    if request.method == "POST":
        domain_name = request.form.get("domain_name")

        if domain_name:
            existing = Domain.query.filter_by(domain_name=domain_name).first()

            if existing:
                flash("Domain already exists!")
            else:
                doc_root = f"{user.home_directory}/{domain_name}"
                os.makedirs(doc_root, exist_ok=True)

                try:
                    shutil.chown(user.home_directory, user=1000, group=1000)
                    shutil.chown(doc_root, user=1000, group=1000)
                except Exception as e:
                    print(f"Chown failed for {doc_root}: {e}")

                index_path = os.path.join(doc_root, "index.html")
                if not os.path.exists(index_path):
                    with open(index_path, "w") as f:
                        f.write(f"# Welcome to {domain_name}!\n\nYour server is ready.\n")

                try:
                    shutil.chown(index_path, user=1000, group=1000)
                except Exception as e:
                    print(f"Chown failed for {index_path}: {e}")

                db_name = make_safe_db_name(domain_name)
                db_user = make_safe_db_user(domain_name)
                db_password = make_db_password(user.username)

                root_user = current_app.config["MYSQL_ROOT_USER"]
                root_password = urllib.parse.quote_plus(current_app.config["MYSQL_ROOT_PASSWORD"])
                mysql_host = current_app.config["MYSQL_HOST"]
                mysql_port = current_app.config["MYSQL_PORT"]

                admin_engine = create_engine(
                    f"mysql+pymysql://{root_user}:{root_password}@{mysql_host}:{mysql_port}/mysql"
                )

                try:
                    with admin_engine.begin() as conn:
                        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
                        conn.execute(
                            text(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY :pwd"),
                            {"pwd": db_password}
                        )
                        conn.execute(
                            text(f"ALTER USER '{db_user}'@'%' IDENTIFIED BY :pwd"),
                            {"pwd": db_password}
                        )
                        conn.execute(text(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%'"))
                        conn.execute(text("FLUSH PRIVILEGES"))

                    new_domain = Domain(
                        domain_name=domain_name,
                        document_root=doc_root,
                        active=True,
                        user_id=user_id
                    )

                    new_database = Database(
                        db_name=db_name,
                        db_user=db_user,
                        db_password=db_password,
                        user_id=user_id
                    )

                    db.session.add(new_domain)
                    db.session.add(new_database)
                    db.session.commit()

                    flash(f"New server deployed successfully! DB: {db_name}")
                    return redirect(url_for("dashboard.dashboard"))

                except Exception as e:
                    db.session.rollback()
                    flash(f"Error creating domain/database: {e}")

        return redirect(url_for("dashboard.dashboard"))

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

    return render_template(
        "dashboard/dashboard.html",
        domains=domains,
        databases=databases,
        db_version=db_version
    )


@dashboard_bp.route("/dashboard/<int:service_id>", methods=["GET", "POST"])
def individual_dashboard(service_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    domain = Domain.query.get_or_404(service_id)

    if domain.user_id != session["user_id"]:
        flash("Unauthorized access!")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "toggle_status":
            old_root = domain.document_root

            if domain.active:
                new_root = old_root.rstrip("/") + "_disabled"
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
                if old_root.endswith("_disabled"):
                    new_root = old_root[:-9]
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
                    domain.active = True

            db.session.commit()
            status_text = "stopped" if not domain.active else "started"
            flash(f"Domain {domain.domain_name} has been {status_text}.")
            return redirect(url_for("dashboard.individual_dashboard", service_id=domain.domain_id))

        elif action == "destroy_server":
            domain_name = domain.domain_name
            try:
                shutil.rmtree(domain.document_root)
            except Exception as e:
                print(f"Failed to remove directory {domain.document_root}: {e}")

            db.session.delete(domain)
            db.session.commit()
            flash(f"Server {domain_name} has been destroyed.")
            return redirect(url_for("dashboard.dashboard"))

        return redirect(url_for("dashboard.individual_dashboard", service_id=domain.domain_id))

    return render_template("dashboard/individual.html", domain=domain)