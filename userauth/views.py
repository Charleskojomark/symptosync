from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # This can be email or username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='userauth.authentication.EmailBackend')
            return redirect('userauth:home')  
        else:
            # Handle invalid login
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'auth/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user, backend='userauth.authentication.EmailBackend')  
            return redirect('home')  
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('userauth:login') 


def home_view(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['email'] = request.user.email
    return render(request, 'auth/home.html', context)