from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from productapp.models import Shop


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})

    trending_products = Shop.objects.filter(cat='trending').order_by('-created_at')[:6]


    return render(request, "home.html",{'trending_products': trending_products})


def demo(request):
    return render(request, "demo.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('credentials:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('credentials:register')
            else:
                user = User.objects.create_user(username=username, password=password,
                                                 email=email)
                user.save()
                print("User created")
                return redirect('credentials:home')
        else:
            messages.info(request, "Passwords do not match")
            return redirect('credentials:register')
    return render(request, "register.html")


def logout_view(request):
    auth.logout(request)
    return redirect('credentials:home')





def index(request):
    return render (request,"index.html")


