<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
    <link rel="stylesheet" href="/todoapp/public/css/style.css">

</head>
<body>
    <h1>ToDo App</h1>

    <!-- Task Input Form -->
    <div>
        <input type="text" id="task-title" placeholder="Task Title" />
        <textarea id="task-desc" placeholder="Task Description"></textarea>
        <button class="btn-add" id="add-task-btn">Add New Task</button>
    </div>

    <!-- Task Lists -->
    <h2>Pending Tasks</h2>
    <ul class="todo-list" id="pending-tasks"></ul>

    <h2>Completed Tasks</h2>
    <ul class="todo-list" id="completed-tasks"></ul>

    <script src="/todoapp/public/js/script.js"></script>
</body>
</html>