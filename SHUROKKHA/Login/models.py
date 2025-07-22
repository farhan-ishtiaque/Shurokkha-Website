from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
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

