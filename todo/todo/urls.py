from django.contrib import admin
from django.urls import path, include

# URL configuration - maps URLs to views
urlpatterns = [
    # Admin URL - gives access to Django's built-in admin interface
    path('admin/', admin.site.urls),
    
    # Root URL - includes URL patterns from the 'todoapp' application
    # This will route requests from the root URL ('/') to 'todoapp' URLs
    path('', include('todoapp.urls')),
    
    # Authentication URL - includes URL patterns from the 'authtodo' application
    # This will route requests starting with 'auth/' to 'authtodo' URLs
    path('auth/', include('authtodo.urls')),
]
