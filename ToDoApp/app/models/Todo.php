<?php
require_once('/Applications/XAMPP/xamppfiles/htdocs/todoapp/config/database.php');

class Todo {
    private $conn;

    public function __construct($conn) {
        $this->conn = $conn;
    }

    public function getAll() {
        try {
            $stmt = $this->conn->query('SELECT * FROM tasks ORDER BY id DESC');
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            error_log($e->getMessage()); 
            return [];
        }
    }

    public function create($title, $description) {
        try {
            $title = htmlspecialchars(trim($title), ENT_QUOTES, 'UTF-8');
            $description = htmlspecialchars(trim($description), ENT_QUOTES, 'UTF-8');

            if (empty($title) || empty($description)) {
                throw new Exception('Title and description cannot be empty.');
            }

            $stmt = $this->conn->prepare('INSERT INTO tasks (title, description) VALUES (?, ?)');
            return $stmt->execute([$title, $description]);
        } catch (Exception $e) {
            error_log($e->getMessage()); 
            return false;
        }
    }

    public function update($id, $title, $description, $is_completed) {
        try {
  
            $id = (int)$id;
            $title = htmlspecialchars(trim($title), ENT_QUOTES, 'UTF-8');
            $description = htmlspecialchars(trim($description), ENT_QUOTES, 'UTF-8');
            $is_completed = (bool)$is_completed;

            if (empty($title) || empty($description)) {
                throw new Exception('Title and description cannot be empty.');
            }

            $stmt = $this->conn->prepare(
                'UPDATE tasks SET title = ?, description = ?, is_completed = ? WHERE id = ?'
            );
            return $stmt->execute([$title, $description, $is_completed, $id]);
        } catch (Exception $e) {
            error_log($e->getMessage()); 
            return false;
        }
    }

    public function delete($id) {
        try {
            $id = (int)$id; // Sicherstellen, dass es ein Integer ist

            $stmt = $this->conn->prepare('DELETE FROM tasks WHERE id = ?');
            return $stmt->execute([$id]);
        } catch (Exception $e) {
            error_log($e->getMessage()); // Fehler protokollieren
            return false;
        }
    }
}
?>
