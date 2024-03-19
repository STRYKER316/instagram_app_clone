from django.shortcuts import redirect, render

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from users.serializers import (
    UserCreateSerializer,
    UserProfileUpdateSerializer,
    UserProfileViewSerializer,
)

from .models import User, UserProfile
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
    userSerializer = UserCreateSerializer(data=request.data)

    response_data = {
        "errors": None,
        "data": None
    }

    if userSerializer.is_valid():
        user = userSerializer.save()

        refresh = RefreshToken.for_user(user)

        response_data["data"] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response_status = status.HTTP_201_CREATED

    else:
        response_data["errors"] = userSerializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):

    print("request user object -> ", request.user)

    user_profiles = UserProfile.objects.all()

    seriliazed_user_profiles = UserProfileViewSerializer(instance=user_profiles, many=True)

    return Response(seriliazed_user_profiles.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, pk):

    print(request.data)

    user = UserProfile.objects.filter(id=pk).first()

    if user:
        seriliazed_user = UserProfileViewSerializer(instance=user)

        response_data = {
            'data': seriliazed_user.data,
            'errors': None
        }
        response_status = status.HTTP_200_OK
    else:
        response_data = {
            'data': None,
            'errors': "User not found"
        }
        response_status = status.HTTP_404_NOT_FOUND

    return Response(response_data, response_status)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):

    print(request.data)
    print(request.user)

    user_profile_serializer = UserProfileUpdateSerializer(
        instance=request.user.profile,
        data=request.data
    )

    response_data = {
        'data': None,
        'errors': None
    }

    if user_profile_serializer.is_valid():
        user_profile = user_profile_serializer.save()
        response_data['data'] = UserProfileViewSerializer(instance=user_profile).data
        response_status = status.HTTP_200_OK

    else:
        response_data['errors'] = user_profile_serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, response_status)
