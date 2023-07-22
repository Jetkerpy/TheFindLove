import uuid

from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .utils import validate_age
from .validators import validate_email, validate_uzb_phone_number

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('status', 'ADMINISTRATOR')


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )

        return self.create_user(email, password, **other_fields)


    
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email = email, **other_fields)

        user.set_password(password)
        user.save()
        return user


class ProfileQueryset(models.QuerySet):
    """
        THIS IS ONLY RETURN QUERYSET OBJECT
        IF OBJECT'S STATUS = "PAYDALANIWSHI"
        AND IS_ACTIVE = "TRUE"
    """
    def users(self):
        return self.filter(user__status = "PAYDALANIWSHI")





class UserBase(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("A'YEL", 'A\'yel'),
        ("ERKEK", 'Erkek'),
    )


    STATUS_OF_USER = (
        ('PAYDALANIWSHI', 'Paydalaniwshi'),
        ('ADMINISTRATOR', 'Administrator'),
    )

    email = models.EmailField(_('Email address'), unique=True, validators=[validate_email])
    first_name = models.CharField(_("Paydalaniwshinin' ati"), max_length=255)
    last_name = models.CharField(_("Paydalaniwshinin' familiyasi"), max_length=255)
    middle_name = models.CharField(_("Paydalaniwshinin a'kesinin' ati"), max_length=255)
    phone_number = models.CharField(max_length=255, unique=True, validators=[validate_uzb_phone_number])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthday = models.DateField(_("Tuwilg'an kuni"), blank=True, null=True, validators=[validate_age])
    face = ResizedImageField(_("Insannin' ju'zi"), upload_to="faces/", null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_OF_USER, default='PAYDALANIWSHI')
    token = models.CharField(_("Tasdiyiqlaw ushin 6 xanali san"), max_length=6, null=True, blank=True)

    #User status
    is_human = models.BooleanField(_("Eger insannin' ju'zi bolsa haqiqiy insan."), default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'
    
    def __str__(self):
        return f'{self.email} & id is {self.pk}'


    @property
    def user_name(self):
        return f"#{self.first_name}"

    @property
    def added_name(self):
        return f"@{self.last_name.lower()}{self.first_name.lower()}"




class Profile(models.Model):
    STATUS_OF_PERSON = (
        ('UYLENBEGEN', 'UYLENBEGEN'),
        ("TURMISQA SHIQPAG'AN", "TURMISQA SHIQPAG'AN"),
        ("AJRASQAN", "AJRASQAN"),
        ("BOS EMES", "BOS EMES"),
        ("BAXTIN TAPQAN", "BAXTIN TAPQAN")
    )

    POSITION = (
        ('JUMIS', 'JUMIS'),
        ('JUMISSIZ', 'JUMISSIZ'),
        ('STUDENT', 'STUDENT'),
        ('BASQA', 'BASQA')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    hobbies = models.ManyToManyField('Hobby', related_name='hobby_of_user')
    bio = models.TextField(_("Ozi haqqida mag'liwmat"), max_length=1000)
    status = models.CharField(max_length=25, choices=STATUS_OF_PERSON)
    address = models.CharField(max_length=255)
    #height = models.FloatField(_("Insannin' boyi"), blank=True) # NEGE DUR QAYTE TUSINBEDIM
    position = models.CharField(max_length=15, choices=POSITION)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager() # Default Manager
    people = ProfileQueryset.as_manager()

    def __str__(self):
        return self.user.email



class Hobby(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Media(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(upload_to='images/')
    alt = models.CharField(_("Image haqida qisqasha mag'liwmat"), max_length=255)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.user.user_name