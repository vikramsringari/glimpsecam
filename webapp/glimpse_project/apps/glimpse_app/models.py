from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email_address = models.CharField(max_length = 45)
    device_key = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Device(models.Model):
    device_owner = models.ForeignKey(User, related_name="devices")
    device_key_name = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Media(models.Model):
    media_type = models.CharField(max_length=10)# either jpeg, or mp4
    uploader = models.ForeignKey(User, related_name="uploads")
    created_at = models.DateTimeField(auto_now_add=True)
