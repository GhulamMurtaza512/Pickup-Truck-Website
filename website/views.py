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

# =====================================================
# DELIVERY DETAIL / TRACKING
# =====================================================

def delivery_detail(request, delivery_id):

    access_token = request.session.get(
        'delivery_access_token'
    )

    delivery = Delivery.objects.filter(
        delivery_id=delivery_id,
        access_token=access_token
    ).first()

    if not delivery:
        messages.error(
            request,
            'Delivery not found.'
        )
        return redirect('my_deliveries')

    return render(
        request,
        'website/delivery_detail.html',
        {
            'delivery': delivery
        }
    )
# =====================================================
# DRIVER PANEL
# =====================================================

def driver_panel(request):

    deliveries = Delivery.objects.all().order_by('-created_at')

    return render(
        request,
        'website/driver_panel.html',
        {
            'deliveries': deliveries
        }
    )

# =====================================================
# UPDATE DELIVERY STATUS
# =====================================================

def update_delivery_status(request, delivery_id):

    if request.method == 'POST':

        delivery = Delivery.objects.filter(
            delivery_id=delivery_id
        ).first()

        if not delivery:
            messages.error(
                request,
                'Delivery not found.'
            )
            return redirect('driver_panel')

        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'accepted',
            'going_to_pickup',
            'picked_up',
            'on_the_way',
            'delivered',
            'cancelled',
        ]

        if new_status not in valid_statuses:

            messages.error(
                request,
                'Invalid delivery status.'
            )

            return redirect('driver_panel')

        delivery.status = new_status
        delivery.save()

        messages.success(
            request,
            f'Delivery {delivery.delivery_id} status updated successfully.'
        )

    return redirect('driver_panel')

# =====================================================
# ASSIGN DRIVER
# =====================================================

def assign_driver(request, delivery_id):

    if request.method == 'POST':

        delivery = Delivery.objects.filter(
            delivery_id=delivery_id
        ).first()

        if not delivery:
            messages.error(
                request,
                'Delivery not found.'
            )
            return redirect('driver_panel')

        driver_name = request.POST.get(
            'assigned_driver',
            ''
        ).strip()

        delivery.assigned_driver = driver_name
        delivery.save()

        messages.success(
            request,
            f'Driver assigned to {delivery.delivery_id}.'
        )

    return redirect('driver_panel')