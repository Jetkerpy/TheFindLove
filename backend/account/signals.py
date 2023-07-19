from apiip import apiip  #pip install apiip
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .hobby import HobbySession
from .models import Profile, UserBase
from .session_middleware import get_current_request
from .utils import get_address, get_path_of_image

API_KEY = apiip(settings.GEOLOCATION_API_KEY)
## JOQARIDAG'I API_KEY MEN "hungry**n*a*y@gmail.com" DA
## BAR OK :)



@receiver(post_save, sender = UserBase)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.is_active:
        profile = Profile.objects.create(user = instance)
        is_man = True if instance.gender == 'ERKEK' else False
        region = get_address(API_KEY)
        profile.address = region


        if is_man:
            profile.avatar = get_path_of_image('man')
        else:
            profile.avatar = get_path_of_image('women')

        # GET SESSION
        request = get_current_request()
        if request is not None:
            hobby = HobbySession(request)
            hobbies = [int(_id) for _id in hobby.get_hobbies()]
            profile.hobbies.add(*hobbies)
            hobby.clear()
        # END GET SESSION

        profile.save()