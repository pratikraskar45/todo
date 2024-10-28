from django.urls import path
from todoapp import views  # Importing views from the todoapp application

urlpatterns = [
    # Root URL - points to the index view
    path('', views.index, name="index"),
    
    # To-do list URL - displays all tasks and allows adding new tasks
    path('todolist/', views.todolist, name="todolist"),
    
    # Delete task URL - deletes a specific task by name
    # <str:name> captures the task name as a string parameter
    path('delete-task/<str:name>/', views.DeleteTask, name="delete"),
    
    # Update task URL - marks a specific task as completed by name
    # <str:name> captures the task name as a string parameter
    path('update/<str:name>/', views.Update, name="update"),
]
