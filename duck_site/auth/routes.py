from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")

@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")

@auth_bp.route("/profile")
def profile():
    return render_template("auth/profile.html")

@auth_bp.route("/settings")
def settings():
    return render_template("auth/settings.html")
