from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
# from .forms import ContentForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
            
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')


otp_storage = {}

def generate_otp():
    return random.randint(100000, 999999)

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            otp_storage[user.username] = otp
            
            send_mail(
                'Your OTP Code',
                f'Your OTP for password reset is {otp}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email')
            return redirect('otp_verification')
        except User.DoesNotExist:
            messages.error(request, 'Email not found')
    return render(request, 'forgot_password.html')
            
def otp_verification(request):
    if request.method == "POST":
        otp = request.POST['otp']
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            if str(otp_storage.get(user.username)) == otp:
                messages.success(request, 'OTP verified successfully')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
    return render(request, 'otp_verification.html')


def reset_password(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'reset_password.html')


@login_required
def home(request):
    if request.method == 'POST':
   
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        alternate_phone_number = request.POST.get('alternate_phone_number')
        profile_image = request.FILES.get('profile_image')

        
        if name and phone_number: 
            content = Content(
                user=request.user,
                name=name,
                phone_number=phone_number,
                alternate_phone_number=alternate_phone_number,
                profile_image=profile_image
            )
            content.save()
            messages.success(request, 'Content added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Name and Phone Number are required.')


    content_list = Content.objects.filter(user=request.user)
    return render(request, 'home.html', {'content_list': content_list})

@login_required
def edit_content(request, content_id):
    content = get_object_or_404(Content, id=content_id, user=request.user)  
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            content.delete()
            messages.success(request, 'Contact deleted successfully')
            return redirect('home')
        else:
           
            content.name = request.POST.get('name', content.name)
            content.phone_number = request.POST.get('phone_number', content.phone_number)
            content.alternate_phone_number = request.POST.get('alternate_phone_number', content.alternate_phone_number)
            if 'profile_image' in request.FILES:
                content.profile_image = request.FILES['profile_image']
            content.save()
            messages.success(request, 'Content updated successfully')
            return redirect('home')
    else:
       
        return render(request, 'edit_content.html', {'content': content})