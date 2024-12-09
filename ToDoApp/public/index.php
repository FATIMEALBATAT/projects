<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once '/Applications/XAMPP/xamppfiles/htdocs/todoapp/config/database.php';
require_once '/Applications/XAMPP/xamppfiles/htdocs/todoapp/app/models/Todo.php';

if (!isset($conn)) {
    die('Database connection is not set. Check config/database.php.');
}

$todoModel = new Todo($conn);

$action = $_GET['action'] ?? 'list';
$id = $_GET['id'] ?? null;

if ($action === 'add' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $todoModel->create($_POST['title'], $_POST['description']);
    header('Location: index.php');
    exit();
}

if ($action === 'edit' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $todoModel->update($id, $_POST['title'], $_POST['description'], isset($_POST['is_completed']));
    header('Location: index.php');
    exit();
}

if ($action === 'delete') {
    $todoModel->delete($id);
    header('Location: index.php');
    exit();
}

$todos = $todoModel->getAll();
require '/Applications/XAMPP/xamppfiles/htdocs/todoapp/app/views/todos.php';
