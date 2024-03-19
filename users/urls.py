from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users import views


urlpatterns = [
    path('index/', views.index, name='user_index'),
    path('signup/', views.signup, name='user_signup'),

    # DRF views
    path('add/', views.create_user, name='create_user_api'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify_api'),

    path('login/', TokenObtainPairView.as_view(), name='login_api'),

    path('list/', views.user_list, name='user_list_api'),

    path('<int:pk>/', views.UserprofileDetail.as_view(), name='user_detail_api'),

]
