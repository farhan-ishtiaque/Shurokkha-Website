from django.db import models

class FireStation(models.Model):
    station_id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.postal_code})"

