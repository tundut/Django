from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re

# View đăng ký
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Email không hợp lệ.")
            return redirect("register")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email đã được sử dụng.")
            return redirect("register")

        elif password != confirm_password:
            messages.error(request, "Mật khẩu không khớp.")
            return redirect("register")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Tên người dùng đã tồn tại.")
            return redirect("register")

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Đăng ký thành công. Vui lòng đăng nhập.")
            return redirect('login')

    return render(request, 'register.html')

# View đăng nhập
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If user is authenticated, log them in
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login if authentication fails
    
    return render(request, 'login.html')
