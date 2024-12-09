document.addEventListener('DOMContentLoaded', () => {
    const taskTitleInput = document.getElementById('task-title');
    const taskDescInput = document.getElementById('task-desc');
    const addTaskButton = document.getElementById('add-task-btn');
    const pendingTasksList = document.getElementById('pending-tasks');
    const completedTasksList = document.getElementById('completed-tasks');

    const fetchTasks = async () => {
        try {
            const response = await fetch('http://localhost/todoapp/tasks.php');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Fetched tasks result:', result);

            const tasks = result.data;
            if (!Array.isArray(tasks)) {
                console.error('Expected "data" to be an array but got:', tasks);
                throw new Error('Invalid response format');
            }

     
            pendingTasksList.innerHTML = '';
            completedTasksList.innerHTML = '';

            let hasPendingTasks = false; 
            const completedTasks = []; 

            tasks.forEach((task, index) => {
                if (!task || typeof task !== 'object' || !task.title || !task.description) {
                    console.warn(`Skipping invalid task at index ${index}:`, task);
                    return; 
                }

                const taskElement = document.createElement('li');
                taskElement.innerHTML = `
                    <strong>${task.title}</strong>
                    <p>${task.description}</p>
                    ${
                        task.status === 'pending'
                            ? `<button class="btn-delete" data-id="${task.id}">Mark as Done</button>`
                            : ''
                    }
                `;
                taskElement.classList.add(
                    task.status === 'completed' ? 'completed' : 'pending'
                );

                if (task.status === 'pending') {
                    hasPendingTasks = true; 
                    pendingTasksList.appendChild(taskElement);
                    taskElement
                        .querySelector('.btn-delete')
                        .addEventListener('click', () =>
                            markTaskAsDone(task.id, taskElement)
                        );
                } else {
                    completedTasks.push(taskElement); 
                }
            });

           
            if (!hasPendingTasks) {
                const noTasksMessage = document.createElement('li');
                noTasksMessage.textContent = 'Currently no pending tasks.';
                noTasksMessage.style.fontStyle = 'italic';
                noTasksMessage.style.color = '#777';
                pendingTasksList.appendChild(noTasksMessage);
            }

            
            renderCompletedTasks(completedTasks);
        } catch (error) {
            console.error('Error fetching tasks:', error);
            alert('Failed to fetch tasks. Please try again.');
        }
    };

    const renderCompletedTasks = (completedTasks) => {
        const MAX_VISIBLE = 5; 
        let showingAll = false; 

        const updateCompletedTasksView = () => {
            completedTasksList.innerHTML = ''; 
            const tasksToShow = showingAll
                ? completedTasks
                : completedTasks.slice(0, MAX_VISIBLE);

            tasksToShow.forEach((task) => completedTasksList.appendChild(task));

            if (completedTasks.length > MAX_VISIBLE) {
                const toggleButton = document.createElement('button');
                toggleButton.textContent = showingAll ? 'Show Less' : 'Show More';
                toggleButton.classList.add('btn-primary'); 

               
                toggleButton.addEventListener('click', () => {
                    showingAll = !showingAll; 
                    updateCompletedTasksView(); 
                });

                completedTasksList.appendChild(toggleButton);
            }
        };

       
        updateCompletedTasksView();
    };

    const addTask = async () => {
        const title = taskTitleInput.value.trim();
        const description = taskDescInput.value.trim();

        if (!title || !description) {
            alert('Please fill in both title and description!');
            return;
        }

        try {
            const response = await fetch('http://localhost/todoapp/tasks.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, description }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                const noTasksMessage = pendingTasksList.querySelector(
                    'li[style*="italic"]'
                );
                if (noTasksMessage) {
                    noTasksMessage.remove();
                }

                const task = result.task;
                const taskElement = document.createElement('li');
                taskElement.innerHTML = `
                    <strong>${task.title}</strong>
                    <p>${task.description}</p>
                    <button class="btn-delete" data-id="${task.id}">Mark as Done</button>
                `;
                taskElement.classList.add('pending');
                pendingTasksList.appendChild(taskElement);

                taskElement
                    .querySelector('.btn-delete')
                    .addEventListener('click', () =>
                        markTaskAsDone(task.id, taskElement)
                    );

                taskTitleInput.value = '';
                taskDescInput.value = '';
            } else {
                alert(result.message || 'Failed to add task.');
            }
        } catch (error) {
            console.error('Error adding task:', error);
            alert('Failed to add task. Please try again.');
        }
    };

    const markTaskAsDone = async (id, taskElement) => {
        try {
            const response = await fetch('http://localhost/todoapp/tasks.php', {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, status: 'completed' }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                pendingTasksList.removeChild(taskElement);
                taskElement.querySelector('.btn-delete').remove();
                taskElement.classList.remove('pending');
                taskElement.classList.add('completed');
                fetchTasks(); 
            } else {
                alert(result.message || 'Failed to update task status.');
            }
        } catch (error) {
            console.error('Error marking task as done:', error);
            alert('Failed to update task status. Please try again.');
        }
    };

    addTaskButton.addEventListener('click', addTask);
    fetchTasks();
});
