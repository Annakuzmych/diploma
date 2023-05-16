from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.db import migrations
from django.contrib.auth import get_user_model
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT,null=True, blank=True)



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
    is_permanent_donor = models.BooleanField(default=False)
    last_donation_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donors_created'
    )

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

    def __str__(self):
        return f"Request for {self.donor} on {self.donation_date}"


class Rejection(models.Model):
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, default=None)
    reason = models.TextField()
    unavailability_term = models.DateTimeField()

    def __str__(self):
        return f"{self.blood_request.donor} rejected for {self.reason}"


