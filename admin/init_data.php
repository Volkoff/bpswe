<?php
// connection to  PostgreSQL through  Unix socket
$conn = pg_connect("host=/var/run/postgresql dbname=hosting user=postgres");

if (!$conn) {
    die("chyba připojení k databázi");
}

// users data
$users = [
    ['user1', 'user1@test.cz', 'hash123', 'user', '/var/www/user1']
];

foreach ($users as $row) {
    $sql = "INSERT INTO users (username, email, password_hash, role, home_directory)
            SELECT '{$row[0]}', '{$row[1]}', '{$row[2]}', '{$row[3]}', '{$row[4]}'
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE username = '{$row[0]}'
            )";
    pg_query($conn, $sql);
}

// plans data
$plans = [
    ['Basic', 2.99, 30]
];

foreach ($plans as $plan) {
    $sql = "INSERT INTO plans (name, price, expire_days)
            SELECT '{$plan[0]}', {$plan[1]}, {$plan[2]}
            WHERE NOT EXISTS (
                SELECT 1 FROM plans WHERE name = '{$plan[0]}'
            )";
    pg_query($conn, $sql);
}

// domain data
$domains = [
    ['www.mojefirma.cz', '/var/www/user1/site1', 1]
];

foreach ($domains as $domain) {
    $sql = "INSERT INTO domains (domain_name, document_root, user_id)
            SELECT '{$domain[0]}', '{$domain[1]}', {$domain[2]}
            WHERE NOT EXISTS (
                SELECT 1 FROM domains WHERE domain_name = '{$domain[0]}'
            )";
    pg_query($conn, $sql);
}

// FTP-accounts
$ftp_accounts = [
    ['ftpuser1', 'hash123', '/var/www/user1', 1000, 1]
];

foreach ($ftp_accounts as $ftp) {
    $sql = "INSERT INTO ftp_accounts (username, password_hash, directory, quota, user_id)
            SELECT '{$ftp[0]}', '{$ftp[1]}', '{$ftp[2]}', {$ftp[3]}, {$ftp[4]}
            WHERE NOT EXISTS (
                SELECT 1 FROM ftp_accounts WHERE username = '{$ftp[0]}'
            )";
    pg_query($conn, $sql);
}

echo "Automatické načítání dat dokončeno";
?>

