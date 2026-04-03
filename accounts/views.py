from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from .models import User

# Create your views here.


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # username OR email
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and (user.is_superuser or user.is_admin):
            login(request, user)
            
            return redirect(reverse('administrator:dashboard'))
        else:
            return render(request, 'accounts/admin_login.html', {
                'error': 'Invalid credentials or not an admin'
            })

    return render(request, 'accounts/admin_login.html')


def user_logout(request):
    logout(request)
    return redirect('/accounts/admin-login/')



def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ✅ check username
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists'
            })

        # ✅ check email
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Email already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_patient = True
        user.save()

        login(
            request,
            user,
            backend='accounts.backends.EmailOrUsernameBackend'
        )

        return redirect('/')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # email OR username
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'accounts/login.html')