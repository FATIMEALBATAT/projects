<?php
require_once 'config.php'; // Externe Konfigurationsdatei

try {
    // Sichere PDO-Verbindung herstellen
    $conn = new PDO(
        "mysql:host=localhost;dbname=todo_app;charset=utf8mb4",
        DB_USERNAME, // Aus config.php
        DB_PASSWORD, // Aus config.php
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // Fehler als Ausnahme
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // Standard-Fetch-Modus
            PDO::ATTR_EMULATE_PREPARES => false, // Native Prepared Statements
        ]
    );

    // Verbindungsprüfung
    $conn->query("SELECT 1");

} catch (PDOException $e) {
    // Fehler sicher behandeln
    error_log("Database connection failed: " . $e->getMessage()); // Fehler protokollieren
    http_response_code(500); // Serverfehler-Code
    echo json_encode(['success' => false, 'message' => 'Database connection failed. Please try again later.']);
    exit();
}
?>
