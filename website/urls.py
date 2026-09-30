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
    path(
    'driver-panel/',
    views.driver_panel,
    name='driver_panel'
),

    path(
    'driver-panel/update-status/<str:delivery_id>/',
    views.update_delivery_status,
    name='update_delivery_status'
),

    path(
    'driver-panel/assign-driver/<str:delivery_id>/',
    views.assign_driver,
    name='assign_driver'
),

]