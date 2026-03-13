from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"  # Change this in production

    # Register blueprints
    from auth.routes import auth_bp
    from dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
