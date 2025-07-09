from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    ]
    DIVISION_CHOICES = [
        ('dhaka', 'Dhaka'),
        ('chittagong', 'Chittagong'),
        ('khulna', 'Khulna'),
        ('rajshahi', 'Rajshahi'),
        ('barisal', 'Barisal'),
        ('sylhet', 'Sylhet'),
        ('mymensingh', 'Mymensingh'),
        ('rangpur', 'Rangpur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, blank=True, null=True)

