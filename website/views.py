from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import (
    Service,
    CustomerProfile,
)


# =====================================================
# HOME
# =====================================================

def home(request):

    services = Service.objects.filter(
        is_active=True
    )

    return render(
        request,
        'website/home.html',
        {
            'services': services
        }
    )


# =====================================================
# ABOUT
# =====================================================

def about(request):

    return render(
        request,
        'website/about.html'
    )


# =====================================================
# CONTACT
# =====================================================

def contact(request):

    return render(
        request,
        'website/contact.html'
    )


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')


    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password'
        )

        remember = request.POST.get(
            'remember'
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            # Remember Me
            if remember:

                request.session.set_expiry(
                    60 * 60 * 24 * 30
                )

            else:

                request.session.set_expiry(
                    0
                )


            return redirect(
                'dashboard'
            )


        messages.error(
            request,
            'Invalid username or password.'
        )


    return render(
        request,
        'website/login.html'
    )


# =====================================================
# REGISTER
# =====================================================

def register(request):

    if request.method == 'POST':

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )


        # ===============================
        # Required Fields
        # ===============================

        if not first_name:
            messages.error(
                request,
                'First name is required.'
            )

            return redirect('register')


        if not username:
            messages.error(
                request,
                'Username is required.'
            )

            return redirect('register')


        if not email:
            messages.error(
                request,
                'Email is required.'
            )

            return redirect('register')


        # ===============================
        # Password Check
        # ===============================

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')


        # ===============================
        # Username Check
        # ===============================

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')


        # ===============================
        # Email Check
        # ===============================

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already exists.'
            )

            return redirect('register')


        # ===============================
        # Create User
        # ===============================

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password,

            first_name=first_name,

            last_name=last_name

        )


        # ===============================
        # Create Customer Profile
        # ===============================

        CustomerProfile.objects.create(

            user=user

        )


        messages.success(
            request,
            'Account created successfully. Please login.'
        )


        return redirect(
            'login'
        )


    return render(
        request,
        'website/register.html'
    )


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):

    logout(request)

    return redirect(
        'home'
    )
# =====================================================
# DASHBOARD
# =====================================================

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    customer, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': ''
        }
    )

    service_requests = customer.service_requests.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'website/dashboard.html',
        {
            'customer': customer,
            'service_requests': service_requests
        }
    )