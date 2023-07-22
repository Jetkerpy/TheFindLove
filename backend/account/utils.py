import random
from datetime import date, timedelta

from django.contrib.gis.geoip2 import GeoIP2
from django.core.exceptions import ValidationError
from django.db import models

#pip install geoip2

def validate_age(value):
    today = date.today()
    adult_age = today - timedelta(days=365 * 18)
    if value > adult_age:
        raise ValidationError("Keshiresiz, dizimnen o'tiwde jasin'iz 18 jastan kishi bolmawi kerek.")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    




def get_address_of_user(request):
    ip_address = get_client_ip(request)
    if ip_address:
        g = GeoIP2()
        local_data = None
        try:
            local_data = g.city(ip_address)
        except:
            pass
    if local_data is not None:
        info = f"{local_data.get('region')}, {local_data.get('country_name')}, {local_data.get('city')}"
        return info
    return "Belgilenbegen."


# def get_ip_address(request):
#     return request.META.get("REMOTE_ADDR")



# def get_address_of_user(api_key, request):
#     ip_address = get_ip_address(request)
#     info = api_key.get_location({"ip": ip_address})
#     return f"{info['countryCode']}, {info['countryName']}, {info['regionName']}, {info['city']}"



def get_path_of_image(image_name):
    guess = random.randrange(1, 6)
    return f"avatars/{image_name}{guess}.jpg"