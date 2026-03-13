from flask import Blueprint, render_template
from models import db, Domain, Database

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
def dashboard():
    # In a real app we'd fetch for the logged-in user, but let's just get everything for now
    domains = Domain.query.all()
    databases = Database.query.all()
    return render_template("dashboard/dashboard.html", domains=domains, databases=databases)

@dashboard_bp.route("/dashboard/<int:service_id>")
def individual_dashboard(service_id):
    domain = Domain.query.get_or_404(service_id)
    return render_template("dashboard/individual.html", domain=domain)
