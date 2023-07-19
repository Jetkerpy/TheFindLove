import random
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import models


def validate_age(value):
    today = date.today()
    adult_age = today - timedelta(days=365 * 18)
    if value > adult_age:
        raise ValidationError("Keshiresiz, dizimnen o'tiwde jasin'iz 18 jastan kishi bolmawi kerek.")



def get_address(api_key):
    info = api_key.get_location()
    return info['regionName']



def get_path_of_image(image_name):
    guess = random.randrange(1, 6)
    return f"avatars/{image_name}{guess}.jpg"