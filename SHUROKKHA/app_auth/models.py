from django.db import models
import uuid

# Create your models here.

class AppUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    nid_number = models.CharField(max_length=20, unique=True)
    Father_name = models.CharField(max_length=50)
    Mother_name = models.CharField(max_length=50)
    address = models.TextField()
    nid_front_image = models.ImageField(upload_to='nid_images/')
    nid_back_image = models.ImageField(upload_to='nid_images/')
    selfie_image = models.ImageField(upload_to='selfie_images/')

    phone_number = models.CharField(max_length=15, unique=True)
    
    password = models.CharField(max_length=128)  # hashed, recommended

    def __str__(self):
        return self.email




class AppUserToken(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='auth_token')
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex  # generate unique token
        return super().save(*args, **kwargs)
        