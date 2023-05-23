from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.db import migrations
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
import secrets
from django.db.models import Sum


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT,default=1, blank=True)
    invitation_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

class Invitation(models.Model):
    sender = models.ForeignKey(ProUser, on_delete=models.CASCADE, default=1)
    email = models.EmailField(default='example@example.com')
    token = models.CharField(max_length=10, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(5)
        super().save(*args, **kwargs)
class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    passport_info = models.CharField(max_length=50)
    last_donation_date = models.DateField(null=True, blank=True)
    donation_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donors_created'
    )
    def update_donation_count(self):
        if not self.is_permanent_donor:
            donation_count = Donation.objects.filter(donor=self).count()
            self.donation_count = donation_count
            self.save()
    @property
    def is_active_donor(self):
        return self.donation_count >= 3

    @property
    def is_permanent_donor(self):
        return self.is_active_donor


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BloodRequest(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='blood_requests')
    analysis = models.TextField()
    pressure = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)
    is_full_donation = models.BooleanField(default=False)
    donation_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(ProUser, on_delete=models.PROTECT)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for {self.donor} on {self.donation_date}"


class Rejection(models.Model):
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, default=None)
    reason = models.TextField()
    unavailability_term = models.DateTimeField()

    def __str__(self):
        return f"{self.blood_request.donor} rejected for {self.reason}"
class Donation(models.Model):
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='donation')
    donation_date = models.DateField(default=timezone.now)
    donation_type = models.CharField(max_length=50)
    plasma_units = models.FloatField(default=0)
    blood_units = models.FloatField(default=0)

    def __str__(self):
        return f"Donation for {self.blood_request} on {self.donation_date}"

