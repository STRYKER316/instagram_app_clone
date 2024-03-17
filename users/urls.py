from django.urls import path

from users import views


urlpatterns = [
    path('index/', views.index, name='user_index'),
    path('signup/', views.signup, name='user_signup'),
]
