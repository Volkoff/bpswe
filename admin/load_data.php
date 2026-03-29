<?php
/**
* Tento skript inicializuje databázi s výchozími daty pro aplikaci.
* Vloží počáteční uživatele, tarify, domény a FTP účty do databáze PostgreSQL.
 */

// connection to PostgreSQL through Unix socket
$conn = pg_connect("host=/var/run/postgresql dbname=hosting user=postgres");

if (!$conn) {
    die("Chyba připojení k databázi!");
}

// Data to insert
$data = [
    ['user1', 'user1@test.cz', 'hash123', 'user', '/var/www/user1']
];

// Inserting into a table users
foreach ($data as $row) {
    $sql = "INSERT INTO users (username, email, password_hash, role, home_directory)
            VALUES ('{$row[0]}', '{$row[1]}', '{$row[2]}', '{$row[3]}', '{$row[4]}')
            ON CONFLICT (username) DO NOTHING"; // so as not to duplicate
    pg_query($conn, $sql);
}

// Inserting a plan
$sql_plan = "INSERT INTO plans (name, price, expire_days)
             VALUES ('Basic', 2.99, 30)
             ON CONFLICT (name) DO NOTHING";
pg_query($conn, $sql_plan);

// Inserting a domain
$sql_domain = "INSERT INTO domains (domain_name, document_root, user_id)
               VALUES ('www.mojefirma.cz', '/var/www/user1/site1', 1)
               ON CONFLICT (domain_name) DO NOTHING";
pg_query($conn, $sql_domain);

// Inserting an FTP account
$sql_ftp = "INSERT INTO ftp_accounts (username, password_hash, directory, quota, user_id)
            VALUES ('ftpuser1', 'hash123', '/var/www/user1', 1000, 1)
            ON CONFLICT (username) DO NOTHING";
pg_query($conn, $sql_ftp);

echo "Данные успешно загружены!";
?>
