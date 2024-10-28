from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# --------------------------------------------------------------------------------------------------------------
# Signup view - handles user registration
def signup(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Retrieve form data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_field = request.POST.get('phone_field')  # phone_field is retrieved but not saved in User model by default
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Password and confirm password do not match.")
            return render(request, 'signup.html')  # Reloads signup page if passwords do not match

        # Check if the email is already taken
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return render(request, 'signup.html')  # Reloads signup page if email exists

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return render(request, 'signup.html')  # Reloads signup page if username exists

        # Create a new user
        try:
            # Using Django's built-in User model to create a user
            my_user = User.objects.create_user(username=username, email=email, password=password)
            my_user.save()  # Saves the new user to the database
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirects to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'signup.html')  # Reloads signup page with error message if an exception occurs

    return render(request, 'signup.html')  # Renders signup page if request method is not POST

# ---------------------------------------------------------------------------------------------------------------------
# Login view - handles user login
def loginpage(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Retrieve login data from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with Django's authenticate function
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Logs the user in if credentials are correct
            messages.success(request, "Login Successful")
            return redirect('index')  # Redirect to home or dashboard after successful login
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')  # Reloads login page if authentication fails

    return render(request, 'login.html')  # Renders login page if request method is not POST

# --------------------------------------------------------------------------------------------------------------------
# Logout view - handles user logout
def logoutpage(request):
    logout(request)  # Logs the user out
    return redirect("login")  # Redirects to login page after logging out
