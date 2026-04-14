from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Domain, FtpAccount
import ftplib
import crypt
import os
import shutil

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid username or password")
            
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("auth.register"))
            
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("auth.register"))
            
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username, 
            email=email, 
            password_hash=hashed_password, 
            role="user", 
            home_directory=f"/var/www/{username}"
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Ensure the user's home directory exists and is owned by the FTP user (UID 1000)
        try:
            os.makedirs(new_user.home_directory, exist_ok=True)
            shutil.chown(new_user.home_directory, user=1000, group=1000)
        except Exception as e:
            print(f"Failed to create/chown home directory {new_user.home_directory}: {e}")
        
        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/register.html")

@auth_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    user = User.query.get(session["user_id"])
    if not user:
        session.pop("user_id", None)
        return redirect(url_for("auth.login"))
        
    # Map domains to appropriate server info format for template
    servers = [
        {"name": dom.domain_name, "status": "Active" if dom.active else "Stopped", "ip": "127.0.0.1 (Local)"} 
        for dom in user.domains
    ]
        
    return render_template("auth/profile.html", user=user, servers=servers)

@auth_bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    if request.method == "POST":
        session["settings"] = {
            "show_console": "show_console" in request.form,
            "show_cpu": "show_cpu" in request.form,
            "show_ram": "show_ram" in request.form,
            "show_disk": "show_disk" in request.form,
        }
        flash("Settings saved successfully!")
        return redirect(url_for("auth.settings"))
        
    user_settings = session.get("settings", {
        "show_console": True,
        "show_cpu": True,
        "show_ram": True,
        "show_disk": True
    })
    
    return render_template("auth/settings.html", settings=user_settings)

@auth_bp.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    user = User.query.get(session["user_id"])
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if not check_password_hash(user.password_hash, old_password):
        flash("Incorrect current password!")
        return redirect(url_for("auth.profile"))
        
    if new_password != confirm_password:
        flash("New passwords do not match!")
        return redirect(url_for("auth.profile"))
        
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    flash("Password updated successfully!")
    return redirect(url_for("auth.profile"))

@auth_bp.route("/ftp", methods=["GET", "POST"])
def ftp_client():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    files = None
    error = None
    
    if request.method == "POST":
        host = request.form.get("host", "ftp")
        username = request.form.get("username")
        password = request.form.get("password")
        
        try:
            # Connect to FTP server
            ftp = ftplib.FTP(timeout=5)
            ftp.connect(host)
            ftp.login(user=username, passwd=password)
            
            # Fetch listing
            files = []
            # retrlines will call the callback for each line.
            ftp.retrlines('LIST', files.append)
            
            ftp.quit()
        except ftplib.all_errors as e:
            error = f"FTP Error: {str(e)}"
            
    return render_template("auth/ftp.html", files=files, error=error)

@auth_bp.route("/ftp/manage", methods=["GET", "POST"])
def ftp_manage():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    user_id = session["user_id"]
    user = User.query.get(user_id)
    domains = Domain.query.filter_by(user_id=user_id).all()
    
    if request.method == "POST":
        action = request.form.get("action", "create")
        
        if action == "create":
            ftp_username = request.form.get("username")
            password = request.form.get("password")
            domain_id = request.form.get("domain_id")
            
            # Simple validation
            if not ftp_username or not password or not domain_id:
                flash("Please fill all required fields")
                return redirect(url_for("auth.ftp_manage"))
                
            # Check if domain belongs to user
            domain = Domain.query.filter_by(domain_id=domain_id, user_id=user_id).first()
            if not domain:
                flash("Invalid domain selection")
                return redirect(url_for("auth.ftp_manage"))
                
            # Check if username already exists
            existing = FtpAccount.query.filter_by(username=ftp_username).first()
            if existing:
                flash("That FTP username is already taken")
                return redirect(url_for("auth.ftp_manage"))
                
            # Generate a secure system hash (SHA512-crypt) with salt
            # This is the standard format ($6$salt$hash) understood by Pure-FTPd
            hashed_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
            new_ftp = FtpAccount(
                username=ftp_username,
                password_hash=hashed_password,
                directory=domain.document_root,
                quota=1024, # default 1GB quota
                user_id=user_id
            )
            db.session.add(new_ftp)
            db.session.commit()
            flash("FTP Account created successfully!")
            
        elif action == "delete":
            account_id = request.form.get("account_id")
            ftp_acc = FtpAccount.query.filter_by(account_id=account_id, user_id=user_id).first()
            if ftp_acc:
                db.session.delete(ftp_acc)
                db.session.commit()
                flash("FTP Account deleted!")
                
        return redirect(url_for("auth.ftp_manage"))
        
    ftp_accounts = FtpAccount.query.filter_by(user_id=user_id).all()
    return render_template("auth/ftp_manage.html", accounts=ftp_accounts, domains=domains)

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
