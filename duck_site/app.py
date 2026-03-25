from flask import Flask, redirect, url_for, session, request
from models import db, User, Domain, Database

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"  # Change this in production
    
    import os
    import urllib.parse
    password = urllib.parse.quote_plus("T!gfwo&*24@!gjw!5%")
    db_host = os.environ.get("DB_HOST", "127.0.0.1")
    db_port = os.environ.get("DB_PORT", "6432")
    app.config["SQLALCHEMY_DATABASE_URI"] = (f"postgresql+psycopg2://student:{password}@{db_host}:{db_port}/hosting_center")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints
    from auth.routes import auth_bp
    from dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    # Global auth guard — only login, register, logout, and static files are public
    @app.before_request
    def require_login():
        allowed_endpoints = {"auth.login", "auth.register", "auth.logout", "index", "static"}
        if request.endpoint not in allowed_endpoints and "user_id" not in session:
            return redirect(url_for("auth.login"))

    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("dashboard.dashboard"))
        return redirect(url_for("auth.login"))

    # Connecting to the local database; removed dummy data initialization to avoid altering data.
    with app.app_context():
        pass
        # db.create_all() ... (dummy data initialization removed)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)
