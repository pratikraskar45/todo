from django.shortcuts import render, redirect
from .models import todo  # Importing the todo model to interact with the database
from django.db import IntegrityError
from django.contrib import messages

# ==================================================================
# Index view - renders the main page
def index(request):
    return render(request, "index.html")  # Renders the main index page for the application

# ==================================================================
# todolist view - handles displaying, creating, and adding tasks
def todolist(request):
    # Check if the request is a POST request (indicating form submission)
    if request.method == 'POST':
        task = request.POST.get('task')  # Retrieve the task name from the form
        if task:  # Only create if the task is not empty
            # Check if the task already exists for the user
            if todo.objects.filter(user=request.user, todo_name=task).exists():
                messages.error(request, "This task already exists.")  # Show error if task already exists
            else:
                # Create a new to-do task with the current user as the owner
                new_todo = todo(user=request.user, todo_name=task)
                new_todo.save()  # Save the new task to the database
    
    # Retrieve all to-do items for the current user
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos  # Pass the list of tasks to the template
    }
    return render(request, "todo.html", context)  # Render the to-do list page with all tasks

# ==================================================================

# DeleteTask view - handles deleting a specific task
def DeleteTask(request, name):
    try:
        # Retrieve the task by name and user to ensure the user only deletes their own tasks
        get_todo = todo.objects.get(user=request.user, todo_name=name)
        get_todo.delete()  # Delete the task from the database
    except todo.DoesNotExist:
        pass  # If the task doesn't exist, do nothing (optional: add a message to inform the user)

    return redirect('todolist')  # Redirect back to the to-do list page

# Update view - marks a task as completed
def Update(request, name):
    # Retrieve the specific to-do item by name and user
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True  # Set the task status to completed
    get_todo.save()  # Save the updated status to the database
    return redirect('todolist')  # Redirect back to the to-do list page
