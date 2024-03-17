from django.http import HttpResponse
from django.shortcuts import render

from .models import User


# Create your views here.
def index(request):
    user_count = User.objects.count()

    return render(request, 'users/index.html')


def signup(request):
    return render(request, 'users/signup.html')
