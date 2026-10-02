from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),
    path('services/', views.services, name='services'),

 path(
    'services/1-ton-pickup-dubai/',
    views.one_ton_pickup,
    name='one_ton_pickup'
),

path(
    'services/pickup-truck-delivery-dubai/',
    views.pickup_delivery,
    name='pickup_delivery'
),

path(
    'services/loading-unloading-labour-dubai/',
    views.loading_labour,
    name='loading_labour'
),

path('robots.txt', views.robots_txt, name='robots_txt'),

path(
    'google61ddc56d63cfcd90.html',
    views.google_verification,
    name='google_verification'
),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
    'service-request/create/',
    views.create_service_request,
    name='create_service_request'
),



]