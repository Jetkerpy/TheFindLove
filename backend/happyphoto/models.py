from django.db import models
from django_resized import ResizedImageField
# Create your models here.


class HappyPhoto(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = ResizedImageField(upload_to='happy_images/')

    def __str__(self):
        return self.title