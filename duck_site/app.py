from flask import Flask, redirect, url_for
from models import db, User, Domain, Database

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"  # Change this in production
    
    import urllib.parse
    password = urllib.parse.quote_plus("T!gfwo&*24@!gjw!5%")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://student:{password}@localhost:5432/hosting_center"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints
    from auth.routes import auth_bp
    from dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # Connecting to the local database; removed dummy data initialization to avoid altering data.
    with app.app_context():
        pass
        # db.create_all() ... (dummy data initialization removed)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
