CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(6),
    home_directory VARCHAR(500)
) ENGINE=InnoDB;

CREATE TABLE plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    price DECIMAL(5,2),
    expire_days INT
) ENGINE=InnoDB;

CREATE TABLE domains (
    domain_id INT AUTO_INCREMENT PRIMARY KEY,
    domain_name VARCHAR(100) UNIQUE NOT NULL,
    document_root VARCHAR(500),
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE user_databases (
    db_id INT AUTO_INCREMENT PRIMARY KEY,
    db_name VARCHAR(30) UNIQUE NOT NULL,
    db_user VARCHAR(50),
    db_password VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ftp_accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    directory VARCHAR(500),
    quota INT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE user_plans (
    user_plan_id INT AUTO_INCREMENT PRIMARY KEY,
    start_date TIMESTAMP,
    expire_date TIMESTAMP,
    plan_id INT,
    user_id INT,
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Данные
INSERT INTO users (username, email, password_hash, role, home_directory)
VALUES ('user1', 'user1@test.cz', 'hash123', 'user', '/var/www/user1');

INSERT INTO plans (name, price, expire_days)
VALUES ('Basic', 2.99, 30);

INSERT INTO ftp_accounts (username, password_hash, directory, quota, user_id)
VALUES ('ftpuser1', 'hash123', '/var/www/user1', 1000, 1);
