from django.shortcuts import redirect, render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserCreateSerializer

from .models import User
from .form import UserSignUpForm


# Create your views here.
def index(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count,
    }

    return render(request, 'users/index.html', context)


def signup(request):
    # context object
    context = {
        'form': UserSignUpForm(),
        'errors': [],
        'message': None,
    }

    # check for POST request
    if request.method == 'POST':
        context['form'] = UserSignUpForm(request.POST)

        if context['form'].is_valid():
            user = context['form'].save(commit=False)
            user.save()
            context['message'] = "User created successfully"
            return redirect('user_signup')

        # invalid form
        context['errors'] = context['form'].errors
        return render(request, 'users/signup.html', context)

    # GET request by default
    return render(request, 'users/signup.html', context)


# ----------------- DRF API Views -----------------

@api_view(['POST'])
def create_user(request):
    # print("Data ->", request.data)

    userSerializer = UserCreateSerializer(data=request.data)

    response_data = {
        "errors": None,
        "data": None
    }

    if userSerializer.is_valid():
        user = userSerializer.save()

        response_data["data"] = {
            "id": user.id
        }
        response_status = status.HTTP_201_CREATED

    else:
        response_data["errors"] = userSerializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)
