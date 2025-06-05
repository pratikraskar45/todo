from django.contrib import admin
from .models import todo  # Importing the todo model from the current package


admin.site.register(todo)  
