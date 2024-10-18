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
