import re
from string import ascii_letters

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserBase


class AccountForm(forms.ModelForm):
    FIO = forms.CharField(max_length=255)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    class Meta:
        model = UserBase
        fields = ['FIO', 'email', 'phone_number', 'gender', 'birthday']


    def clean_FIO(self):
        fio = self.cleaned_data['FIO']
        self.__verify_fio(fio)
        return fio


    def clean_password2(self):
        """
        Check two password
        """
        password_regex = r"^(?=.*\d).{8,}$"
        cd = self.cleaned_data
        
        if not re.match(password_regex, cd['password']):
            raise forms.ValidationError("Quramali qilip kiritiwdi soraymiz ha'm keminde uzinlig'i 8 den to'men bolmawi jan'e sannan da ibarat boliwi kerek.")
    
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Kiritilgen password bir-birine ten' emes, qaytadan kiritin!")
        return cd

    
    @classmethod
    def __verify_fio(cls, fio):
        _f = fio.split()
        if len(_f) != 3:
            raise forms.ValidationError("Kiritilgen FIO standartg'a tuwri kelmeydi!")
        
        letters = ascii_letters #abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

        for s in _f:
            if len(s) < 3:
                raise forms.ValidationError("FIO toliq kiritilmegen, toliq kiritiwdi soraymiz!")
            
            if s[0] != s[0].upper():
                raise forms.ValidationError("FIO har birinin' bas ha'ribi u'lken ha'ribten ibarat boliwi kerek!")
            
            if len(s.strip(letters)) != 0:
                raise forms.ValidationError("FIO tek alphabet turinde kiritiwin'iz shart!")
        
    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['FIO'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'FIO'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail'}
        )
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Phone Number'}
        )
        self.fields['gender'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Gender'}
        )
        self.fields['birthday'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Birthday'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'}
        )

    
# LOGIN FORM
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control mb-3",
            "placeholder": "Username",
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password', 
            'id': 'login-password'
        }
    ))

# END LOGIN FORM