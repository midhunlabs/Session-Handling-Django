from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User


# Login
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "app/login.html",
                {"message": "Email or Password incorrect"},
            )

    return render(request, "app/login.html")


# Signup
@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if password != re_password:
            return render(
                request,
                "app/signup.html",
                {"message": "Passwords not matching"},
            )

        if User.objects.filter(username=email).exists():
            return render(
                request,
                "app/signup.html",
                {"message": "Email already exists"},
            )

        User.objects.create_user(
            username=email,
            email=email,
            first_name=name,
            password=password,
        )

        return redirect("login")

    return render(request, "app/signup.html")


# Home
@never_cache
def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "app/home.html")


# Logout
@never_cache
def logout_view(request):
    auth_logout(request)
    return redirect("login")
