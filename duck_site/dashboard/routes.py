from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")

@dashboard_bp.route("/dashboard/<int:service_id>")
def individual_dashboard(service_id):
    return render_template("dashboard/individual.html", service_id=service_id)
