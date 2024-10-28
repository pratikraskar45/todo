from django.urls import path,include
from authtodo import views
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutpage,name="logout")

]
