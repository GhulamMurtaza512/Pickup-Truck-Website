from django.db import models
from django.contrib.auth.models import User

# =====================================================
# SERVICE
# =====================================================

class Service(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='services/'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =====================================================
# CUSTOMER PROFILE
# =====================================================

class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            self.user.get_full_name()
            or self.user.username
        )


# =====================================================
# SERVICE REQUEST / SERVICE HISTORY
# =====================================================

class ServiceRequest(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('confirmed', 'Confirmed'),

        ('in_progress', 'In Progress'),

        ('completed', 'Completed'),

        ('cancelled', 'Cancelled'),

    ]

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests'
    )

    pickup_location = models.CharField(
        max_length=255
    )

    drop_location = models.CharField(
        max_length=255,
        blank=True
    )

    service_date = models.DateField(
        null=True,
        blank=True
    )

    service_time = models.TimeField(
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f'{self.customer} - {self.service}'


# =====================================================
# RATING
# =====================================================

class Rating(models.Model):

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='rating'
    )

    rating = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.customer} - {self.rating} Stars'


# =====================================================
# CUSTOMER REVIEW / COMMENT
# =====================================================

class Review(models.Model):

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f'{self.customer} - {self.rating} Stars'
