from django.urls import path,include
from authtodo import views
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutpage,name="logout"),
    
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.password_reset_sent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.reset_password, name='reset-password'),
    
    # # for send mail
    # path('activate/<uid64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    
    #  # ... other URL patterns ...
    # path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),

]
