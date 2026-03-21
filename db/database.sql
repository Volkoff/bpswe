CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(6),
    home_directory VARCHAR(500)
);
CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    price DECIMAL(5,2),
    expire_days INTEGER
);
CREATE TABLE domains (
    domain_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(100) UNIQUE NOT NULL,
    document_root VARCHAR(500),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(user_id)
);
CREATE TABLE databases (
    db_id SERIAL PRIMARY KEY,
    db_name VARCHAR(30) UNIQUE NOT NULL,
    db_user VARCHAR(50),
    db_password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(user_id)
);
CREATE TABLE ftp_accounts (
    account_id SERIAL PRIMARY KEY,
    username VARCHAR(40) NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    directory VARCHAR(500),
    quota INTEGER,
    user_id INTEGER REFERENCES users(user_id)
);
CREATE TABLE user_plans (
    user_plan_id SERIAL PRIMARY KEY,
    start_date TIMESTAMP,
    expire_date TIMESTAMP,
    plan_id INTEGER REFERENCES plans(plan_id),
    user_id INTEGER REFERENCES users(user_id)
);

INSERT INTO users (username, email, password_hash, role, home_directory)
VALUES ('user1', 'user1@test.cz', 'hash123', 'user', '/var/www/user1');

INSERT INTO plans (name, price, expire_days)
VALUES ('Basic', 2.99, 30);

INSERT INTO domains (domain_name, document_root, user_id)
VALUES ('www.mojefirma.cz', '/var/www/user1/site1', 1);

INSERT INTO ftp_accounts (username, password_hash, directory, quota, user_id)
VALUES ('ftpuser1', 'hash123', '/var/www/user1', 1000, 1);
