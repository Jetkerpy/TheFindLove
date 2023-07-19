from django.contrib import admin

from .models import UserBase, Profile, Hobby, Media

# Register your models here.


admin.site.register(UserBase)
admin.site.register(Profile)
admin.site.register(Hobby)
admin.site.register(Media)