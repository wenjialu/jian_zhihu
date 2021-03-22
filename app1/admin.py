from django.contrib import admin

# Register your models here.
from app1.models import Profile, User, Issue, Answer, Attitude, Comment
# admin.site.unregister(User)
admin.site.register(Profile)
admin.site.register(Issue)
admin.site.register(Answer)
admin.site.register(Attitude)
admin.site.register(Comment)