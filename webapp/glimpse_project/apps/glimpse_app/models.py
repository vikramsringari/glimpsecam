from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
PHONE_REGEX = re.compile(r'^(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['usersName']) <= 2): # | (postData['usersName'].isalpha() != True):
            errors['usersNames'] = ("Please Do Not Leave The Name Field Blank")
        if not EMAIL_REGEX.match(postData['usersEmail']):
            errors['emails'] = ("Please enter a valid email address")
        if User.objects.filter(email_address = postData['usersEmail']):
            errors['emails2'] = ("Please enter an email that hasn't been used already")
        if not PHONE_REGEX.match(postData['usersPhone']):
            errors['phone'] = ("Please enter a valid phone number")
        if User.objects.filter(device_key_name = postData['deviceNumber']):
            errors['phone'] = ("This Device Number Has Already Been Taken")
        # if (len(postData['password']) <= 7):
        #     errors['passwords'] = ("Make sure your password is longer than 8 characters long")
        # if ((postData['password']) != (postData['checkPass'])):
        #     errors['checkpasswords'] = ("Make sure your password matches")
        return errors
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email_address = postData['emailsLogin']):
            errors['emailMismatch'] = ("Make sure you have already registered or are entering your email correctly")
        elif User.objects.filter(email_address = postData['emailsLogin']):
            user = User.objects.get(email_address = postData['emailsLogin'])
            if postData['deviceNumber'] != user.device_key_name:
                errors['checkDevice'] = ("Make sure you enter the correct device number")
        return errors

class User(models.Model):
    full_name = models.CharField(max_length = 45)
    email_address = models.CharField(max_length = 45)
    phone_number = models.CharField(max_length = 45)
    device_key_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Device(models.Model):
    device_owner = models.ForeignKey(User, related_name="devices")
    device_key_name = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Media(models.Model):
    media_type = models.CharField(max_length=10)# either jpeg, or mp4
    uploader = models.ForeignKey(User, related_name="uploads")
    created_at = models.DateTimeField(auto_now_add=True)
