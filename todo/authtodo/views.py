from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.views import View
from .models import PasswordReset
from .utils import generate_token
import re
from django.core.exceptions import ValidationError

# --------------------------------------------------------------------------------------------------------------
def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_field = request.POST.get('phone_field')  
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if password != confirmPassword:
            messages.warning(request, "Password and confirm password do not match")
            return render(request, 'signup.html')  
        
        try:
            validate_password_strength(password)  
        except ValidationError as e:    
            messages.warning(request, str(e))
            return render(request, 'signup.html')
        
        if len(password) < 5:
            messages.warning(request, "Password must be at least 5 characters")
            return render(request, 'signup.html')

        
        if User.objects.filter(email=email).exists():
            messages.warning(request, "This email is already taken")
            return render(request, 'signup.html')  

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return render(request, 'signup.html')  

        try:
            my_user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password
            )
            my_user.save()  
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
           
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'signup.html')  

    return render(request, 'signup.html')  

# ---------------------------------------------------------------------------------------------------------------------
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            messages.success(request, "Login Successful")
            return redirect('index')  
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('login') 

    return render(request, 'login.html')  

# --------------------------------------------------------------------------------------------------------------------
def logoutpage(request):
    logout(request)  
    messages.info(request, "Logged out successfully")
    return redirect("login")  
# --------------------------------------------------------------------------------------------------------------------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

        new_password_reset = PasswordReset(user=user)
        new_password_reset.save()

        password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
        full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

        email_body = f'Reset your password using the link below:\n\n{full_password_reset_url}'
        email_message = EmailMessage(
            'Reset your password',
            email_body,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.fail_silently = True
        email_message.send()

        return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

    return render(request, 'forgot_password.html')
# --------------------------------------------------------------------------------------------------------------------
def password_reset_sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot-password')
# --------------------------------------------------------------------------------------------------------------------
def reset_password(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'reset_password.html', {'reset_id': reset_id})

            try:
                validate_password_strength(password)  # Validate password strength
            except ValidationError as e:
                messages.warning(request, str(e))
                return render(request, 'reset_password.html', {'reset_id': reset_id})

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                password_reset_id.delete()
                messages.error(request, 'Reset link has expired')
                return redirect('forgot-password')

            user = password_reset_id.user
            user.set_password(password)
            user.save()

            password_reset_id.delete()

            messages.success(request, 'Password reset successful. Proceed to login')
            return redirect('login')

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot-password')

    return render(request, 'reset_password.html', {'reset_id': reset_id})
# --------------------------------------------------------------------------------------------------------------------
# Account activation
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        
        messages.error(request, "Activation link is invalid or expired.")
        return render(request, 'activatefail.html')
    # ---------------------------------------------------------
    #  validate password using the django
def validate_password_strength(password):
    if len(password) <= 5:
        raise ValidationError("Password must be more than 5 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number.")
# -------------------------------------------------------
def password_reset_sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot-password')