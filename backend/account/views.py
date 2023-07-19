import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render


from .forms import AccountForm
from .hobby import HobbySession
from .models import Hobby, Profile, UserBase

# Create your views here.




def register(request):
    hobbies = Hobby.objects.all()
    hobby = HobbySession(request)
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
    
        if form.is_valid():
            user = form.save(commit=False)

            # HOBBIES
            selected_hobbies = list(filter(None, request.POST.getlist('hobbies')[0].split(",")))

            if not selected_hobbies:
                messages.warning(request, "Qizig'iwshilig'in'iz boyisha keminde birewin tan'lawin'iz kerek!")

            # END HOBBIES 

            if selected_hobbies:
                hobby.add(selected_hobbies)
          

                fio = form.cleaned_data.get("FIO").split()
                user.first_name = fio[1]
                user.last_name = fio[0]
                user.middle_name = fio[-1]
                user.set_password(form.cleaned_data.get('password'))
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('happyphoto:home')


    else:
        form = AccountForm()


    context = {
        'form': form,
        'hobbies': hobbies
    }
    return render(request, 'account/sign_up.html', context)



def profiles(request):
    _profiles = Profile.people.users()
    context = {
        'profiles': _profiles
    }
    return render(request, 'account/profiles.html', context)



@login_required
def dashboard(request, id):

    try:
        uuid_object = uuid.UUID(id)
    except ValueError:
        # BUL JERDE MISALI "cfda24c1-b73e-4e4c-95ba-6ef545046ec8" UUID USINDAY BOLADI
        # ENDI KIMDIR SINAP KOREDI OSHIRIP AYRIM JERLERDI 
        # "cfda24c1-b73e-4e4c-6ef545046ec8" KEMIS QILIP REQUEST JIBERIP KOREDI
        # SOL JERDE BIZLER TEKSERIP ATIRMIZ OK 
        # http404() bersek basqa error berip atir nege bilmedim 
        # sonin ushin bizler deploy qilip bir sinap koremiz ok 
        messages.warning(request, 'Sorry, Siz qayte kiritdiniz uuid di!')
        return redirect('/')

    profile = get_object_or_404(Profile, id = uuid_object)

    context = {

    }
    return render(request, 'account/dashboard.html', context)
