from django.shortcuts import redirect, render

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
