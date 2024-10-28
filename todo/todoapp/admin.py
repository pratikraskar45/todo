from django.contrib import admin
from .models import todo  # Importing the todo model from the current package

# Register your models here.
admin.site.register(todo)  # Registers the todo model with the Django admin site
