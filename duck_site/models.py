from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    role = db.Column(db.String(6), nullable=False)
    home_directory = db.Column(db.String(500), nullable=False)

    domains = db.relationship('Domain', backref='owner', lazy=True)
    databases = db.relationship('Database', backref='owner', lazy=True)
    ftp_accounts = db.relationship('FtpAccount', backref='owner', lazy=True)
    user_plans = db.relationship('UserPlan', backref='user', lazy=True)

class Plan(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    expire_days = db.Column(db.Integer, nullable=False)

    user_plans = db.relationship('UserPlan', backref='plan', lazy=True)

class UserPlan(db.Model):
    __tablename__ = "user_plans"

    user_plan_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    expire_date = db.Column(db.Date, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Database(db.Model):
    __tablename__ = "user_databases"

    db_id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(30), nullable=False)
    db_user = db.Column(db.String(50), nullable=False)
    db_password = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Domain(db.Model):
    __tablename__ = "domains"

    domain_id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(100), nullable=False)
    document_root = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class FtpAccount(db.Model):
    __tablename__ = "ftp_accounts"

    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    directory = db.Column(db.String(500), nullable=False)
    quota = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
