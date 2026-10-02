from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.parse import quote
from .models import (
    Service,
    CustomerProfile,
    ServiceRequest,
)
from django.http import HttpResponse


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



def services(request):
    return render(request, 'website/services.html')


def one_ton_pickup(request):
    return render(
        request,
        'website/service_1ton.html'
    )
def pickup_delivery(request):
    return render(
        request,
        'website/service_delivery.html'
    )
def loading_labour(request):
    return render(
        request,
        'website/service_labour.html'
    )


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://pickup-truck-website.onrender.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")

def google_verification(request):
    return HttpResponse(
        "google-site-verification: google61ddc56d63cfcd90.html",
        content_type="text/plain"
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
        defaults={'phone': ''}
    )

    service_requests = customer.service_requests.all().order_by('-created_at')

    services = Service.objects.filter(is_active=True)

    return render(
        request,
        'website/dashboard.html',
        {
            'customer': customer,
            'service_requests': service_requests,
            'services': services,
        }
    )


def create_service_request(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        customer, created = CustomerProfile.objects.get_or_create(
            user=request.user,
            defaults={'phone': ''}
        )

        service_id = request.POST.get('service')
        pickup_location = request.POST.get('pickup_location', '').strip()
        drop_location = request.POST.get('drop_location', '').strip()
        service_date = request.POST.get('service_date')
        service_time = request.POST.get('service_time')
        notes = request.POST.get('notes', '').strip()

        if not service_id:
            messages.error(request, 'Please select a service.')
            return redirect('dashboard')

        if not pickup_location:
            messages.error(request, 'Pickup location is required.')
            return redirect('dashboard')

        if not drop_location:
            messages.error(request, 'Destination is required.')
            return redirect('dashboard')

        if not service_date:
            messages.error(request, 'Service date is required.')
            return redirect('dashboard')

        service = Service.objects.filter(
            id=service_id,
            is_active=True
        ).first()

        if not service:
            messages.error(request, 'Selected service is not available.')
            return redirect('dashboard')

        ServiceRequest.objects.create(
            customer=customer,
            service=service,
            pickup_location=pickup_location,
            drop_location=drop_location,
            service_date=service_date,
            service_time=service_time or None,
            notes=notes,
            status='pending'
        )

        messages.success(
            request,
            'Your service request has been submitted successfully.'
        )

        return redirect('dashboard')

    return redirect('dashboard')

