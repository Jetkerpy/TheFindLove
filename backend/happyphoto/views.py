from django.shortcuts import render
from .models import HappyPhoto

# Create your views here.


def home(request):
    images = HappyPhoto.objects.all()
    context = {
        'images': images
    }
    return render(request, 'happyphoto/home.html', context)



# 404 PAGE
def handler404(request, exception):
    return render(request, '404.html', status=404)
# END 404 PAGE

# 500 SERVER ERROR
def server_error(request):
    return render(request, '500.html', status=500)
# END 500 SERVER ERROR