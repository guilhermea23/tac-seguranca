<?php
declare(strict_types=1);
session_start();

// Security headers
header("X-Frame-Options: DENY");
header("X-Content-Type-Options: nosniff");
header("Content-Security-Policy: default-src 'self'");
header("Referrer-Policy: strict-origin-when-cross-origin");

// Database connection
function getDBConnection(): mysqli
{
    static $conn = null;
    if ($conn === null) {
        $conn = new mysqli(
            getenv('DB_HOST') ?: 'db',
            getenv('DB_USER') ?: 'root',
            getenv('DB_PASS') ?: 'dvwa',
            getenv('DB_NAME') ?: 'dvwa'
        );
        if ($conn->connect_errno) {
            throw new RuntimeException("Database connection failed");
        }
        $conn->set_charset("utf8mb4");
    }
    return $conn;
}

function loginUser(string $username, string $password): bool
{
    $stmt = getDBConnection()->prepare("SELECT id, username, password, is_admin FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();

    if ($user = $stmt->get_result()->fetch_assoc()) {
        if (password_verify($password, $user['password'])) {
            session_regenerate_id(true);
            $_SESSION['user'] = [
                'id' => $user['id'],
                'username' => $user['username'],
                'is_admin' => (bool) $user['is_admin'],
                'ip' => $_SERVER['REMOTE_ADDR'],
                'user_agent' => $_SERVER['HTTP_USER_AGENT']
            ];
            return true;
        }
    }
    return false;
}

function isAdmin(): bool
{
    return $_SESSION['user']['is_admin'] ?? false;
}

function registerUser(array $data): bool
{
    if (strlen($data['username']) < 4)
        throw new InvalidArgumentException("Username must be at least 4 characters");
    if (strlen($data['password']) < 8)
        throw new InvalidArgumentException("Password must be at least 8 characters");

    $stmt = getDBConnection()->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    $stmt->bind_param("ss", $data['username'], password_hash($data['password'], PASSWORD_BCRYPT));
    return $stmt->execute();
}
