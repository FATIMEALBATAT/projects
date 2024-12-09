<!DOCTYPE html>
<html>
<head>
    <title>Add/Edit Task</title>
    <link rel="stylesheet" href="/todoapp/public/css/style.css">
   
</head>
<body>
    <h1><?= $action === 'add' ? 'Add New Task' : 'Edit Task'; ?></h1>
    <form action="?action=<?= $action; ?><?= $id ? "&id=$id" : ''; ?>" method="post">
        <input type="text" name="title" placeholder="Task Title" required>
        <textarea name="description" placeholder="Task Description"></textarea>
        <input type="submit" value="Save">
    </form>
</body>
</html>
