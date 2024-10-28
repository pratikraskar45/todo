from django.db import models
from django.contrib.auth.models import User

# Model for a to-do item
class todo(models.Model):
    # ForeignKey to link each to-do item to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Field to store the name of the to-do task
    todo_name = models.CharField(max_length=1000)
    
    # Boolean field to track the completion status of the task
    status = models.BooleanField(default=False)
    
    # String representation of the model, used for easy identification in the admin panel or console
    def __str__(self):
        return self.todo_name
