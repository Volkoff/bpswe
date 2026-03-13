from flask import Flask, redirect, url_for
from models import db, User, Domain, Database

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"  # Change this in production
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
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

    # Initializing local database with some dummy data so we can see stuff!
    with app.app_context():
        db.create_all()
        
        if not User.query.first():
            test_user = User(username="testuser", email="test@test.com", password_hash="dummyhash", role="user", home_directory="/var/www/testuser")
            db.session.add(test_user)
            db.session.commit()
            
            d1 = Domain(domain_name="example-prod.com", document_root="/var/www/testuser/example", active="Y", user_id=test_user.user_id)
            d2 = Domain(domain_name="dev-staging.net", document_root="/var/www/testuser/dev", active="N", user_id=test_user.user_id)
            db.session.add_all([d1, d2])
            
            db1 = Database(db_name="wp_prod_db", db_user="wp_user", db_password="pwd", user_id=test_user.user_id)
            db2 = Database(db_name="dev_db", db_user="dev_user", db_password="pwd", user_id=test_user.user_id)
            db.session.add_all([db1, db2])
            
            db.session.commit()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
