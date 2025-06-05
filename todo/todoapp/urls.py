from django.urls import path
from todoapp import views  

urlpatterns = [
    path('', views.index, name="index"),
    
    path('todolist/', views.todolist, name="todolist"),
    
    path('delete-task/<str:name>/', views.DeleteTask, name="delete"),
    
    path('update/<str:name>/', views.Update, name="update"),
    
    path('edit/<str:name>/', views.EditTask, name='edit'),

]
