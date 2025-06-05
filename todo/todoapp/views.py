from django.shortcuts import render, redirect,get_object_or_404
from .models import todo  # Importing the todo model to interact with the database
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ==================================================================
@login_required
def index(request):
    return render(request, "index.html")  

# ==================================================================
def todolist(request):
    if request.method == 'POST':
        task = request.POST.get('task')  
        if task:  
            if todo.objects.filter(user=request.user, todo_name=task).exists():
                messages.error(request, "This task already exists.")  
            else:
                new_todo = todo(user=request.user, todo_name=task)
                new_todo.save()  
    
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos  
    }
    return render(request, "todo.html", context)  

# ==================================================================

def DeleteTask(request, name):
    try:
        get_todo = todo.objects.get(user=request.user, todo_name=name)
        get_todo.delete()  
    except todo.DoesNotExist:
        pass  

    return redirect('todolist')  
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True  
    get_todo.save()  
    return redirect('todolist')  
# --------------------------------------------------------------------
def EditTask(request, name):
    task = get_object_or_404(todo, user=request.user, todo_name=name)

    if request.method == 'POST':
        new_name = request.POST.get('task')
        if new_name:
            if todo.objects.filter(user=request.user, todo_name=new_name).exists():
                messages.error(request, "This task already exists.")
                
            else:
                task.todo_name = new_name  
                task.save()  
                return redirect('todolist')

    return render(request, "edit_task.html", {"task": task})