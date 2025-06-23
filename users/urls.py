from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from users.views import UserMeView, UserUpdateView

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('me/update/', UserUpdateView.as_view(), name='user-me-update'),
]


# from .views import (
#     CustomLoginView,
#     CustomSignupView,
#     ProfileView,
#     InviteView,
#     TOTPSetupView,
#     EmailVerificationSentView,
#     SetupOTPView,
#     VerifyOTPView
# )
#
# app_name = 'users'
#
# urlpatterns = [
#      # auth
#     path('accounts/login/', CustomLoginView.as_view(), name='sign_in'),
#     path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
#     path('email-verification-sent/', EmailVerificationSentView.as_view(), name='email_verification_sent'),
#     # path('totp-setup/', TOTPSetupView.as_view(), name='totp_setup'),
#     # path('user_type/', UserTypeView.as_view(), name='user_type'), # убираем
#
#     #2FA
#     path('setup-otp/', SetupOTPView.as_view(), name='setup_otp'),
#     path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
#
#     # кастомный сброс пароля
#     # path('password/reset/', PasswordResetView.as_view(), name='password_reset'), # кастомные views, вместо них allauth
#     # path('password/reset/confirm/<uidb64>/<token>/',
#     #      PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#
#     path('profile_settings/', ProfileView.as_view(), name='profile'),
#
#     # oauth2
#     path('oauth2/', include('allauth.socialaccount.urls')),
# ]