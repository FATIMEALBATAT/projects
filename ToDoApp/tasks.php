<?php
header('Content-Type: application/json');

require_once __DIR__ . '/config/database.php';

if (!isset($conn)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Database connection not established.']);
    exit();
}

$method = $_SERVER['REQUEST_METHOD'];

try {
    if ($method === 'GET') {
        // Aufgaben abrufen
        $query = "SELECT * FROM tasks ORDER BY id DESC";
        $stmt = $conn->prepare($query);
        $stmt->execute();
        $tasks = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // XSS-Schutz bei der Ausgabe (optional)
        $tasks = array_map(function ($task) {
            return [
                'id' => (int)$task['id'],
                'title' => htmlspecialchars($task['title'], ENT_QUOTES, 'UTF-8'),
                'description' => htmlspecialchars($task['description'], ENT_QUOTES, 'UTF-8'),
                'status' => $task['status']
            ];
        }, $tasks);

        echo json_encode(['success' => true, 'data' => $tasks]);
        exit();

    } elseif ($method === 'POST') {
        // Neue Aufgabe hinzufügen
        $data = json_decode(file_get_contents('php://input'), true);

        if (!empty($data['title']) && !empty($data['description'])) {
            $title = trim($data['title']);
            $description = trim($data['description']);

            $query = "INSERT INTO tasks (title, description, status) VALUES (:title, :description, 'pending')";
            $stmt = $conn->prepare($query);
            $stmt->execute([
                'title' => htmlspecialchars($title, ENT_QUOTES, 'UTF-8'), // XSS-Schutz
                'description' => htmlspecialchars($description, ENT_QUOTES, 'UTF-8') // XSS-Schutz
            ]);

            $lastId = $stmt->rowCount() > 0 ? $conn->lastInsertId() : null;

            echo json_encode([
                'success' => true,
                'task' => [
                    'id' => $lastId,
                    'title' => $title,
                    'description' => $description,
                    'status' => 'pending'
                ]
            ]);
        } else {
            http_response_code(400); // Ungültige Eingaben
            echo json_encode(['success' => false, 'message' => 'Invalid input data. Title and description are required.']);
        }
        exit();

    } elseif ($method === 'PATCH') {
        // Aufgabe aktualisieren
        $data = json_decode(file_get_contents("php://input"), true);

        if (isset($data['id'], $data['status']) && in_array($data['status'], ['pending', 'completed'])) {
            $id = filter_var($data['id'], FILTER_VALIDATE_INT);
            if (!$id) {
                http_response_code(400); // Ungültige Eingabe
                echo json_encode(['success' => false, 'message' => 'Invalid task ID.']);
                exit();
            }

            $status = $data['status'];

            $query = "UPDATE tasks SET status = :status WHERE id = :id";
            $stmt = $conn->prepare($query);
            $stmt->execute([
                'status' => $status,
                'id' => $id
            ]);

            echo json_encode(['success' => true, 'message' => 'Task updated successfully!']);
        } else {
            http_response_code(400); // Ungültige Eingabe
            echo json_encode(['success' => false, 'message' => 'Invalid input.']);
        }
        exit();

    } else {
        // Unsupported Method
        http_response_code(405); // Methode nicht erlaubt
        echo json_encode(['success' => false, 'message' => 'Unsupported request method.']);
        exit();
    }
} catch (Exception $e) {
    http_response_code(500); // Serverfehler
    echo json_encode(['success' => false, 'message' => 'Server error occurred.']);
    error_log($e->getMessage()); // Fehler protokollieren
    exit();
}
?>