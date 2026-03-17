from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Domain

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
        {"name": dom.domain_name, "status": "Active" if dom.active == 'Y' else "Stopped", "ip": "127.0.0.1 (Local)"} 
        for dom in user.domains
    ]
        
    return render_template("auth/profile.html", user=user, servers=servers)

@auth_bp.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("auth/settings.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
