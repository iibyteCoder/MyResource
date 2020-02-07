from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=16, blank=False, null=False)
    password = models.CharField(max_length=32, blank=False, null=False)
    email = models.EmailField()
    created_time = models.DateTimeField(auto_now_add=True)


class PersonalProfile(models.Model):
    age = models.IntegerField()
    birthday = models.DateField()
    address = models.TextField()
    profile_img = models.ImageField(upload_to='myresource/upload/profile_photo/')
    user_id = models.ForeignKey(to=Users, on_delete=models.CASCADE)


class DailyRoutine(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    event_special = models.CharField(max_length=16)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    event_color = models.CharField(max_length=16)
    event_editable = models.CharField(max_length=16, default="true")
    event_url = models.CharField(max_length=512, blank=True, null=True)
    event_details = RichTextField(blank=True, null=True)
    event_imgs = models.ImageField(upload_to='myresource/upload/daily_pic/')
    user_id = models.ForeignKey(to=Users, on_delete=models.CASCADE)
