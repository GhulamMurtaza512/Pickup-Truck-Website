from django.shortcuts import render
from .models import Service

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


def about(request):
    return render(request, 'website/about.html')


def contact(request):
    return render(request, 'website/contact.html')


def login_view(request):
    return render(request, 'website/login.html')


def register(request):
    return render(request, 'website/register.html')