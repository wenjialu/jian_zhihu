from django.contrib import admin

# Register your models here.
from app1.models import Profile, User
# admin.site.unregister(User)
admin.site.register(Profile)