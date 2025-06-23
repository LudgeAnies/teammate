# from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from allauth.account.views import LoginView, SignupView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotAuthenticated

from .forms import CustomLoginForm, CustomSignupForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser

from rest_framework import viewsets, permissions
from .serializers import UserSerializer

from rest_framework import generics, status, permissions, views, viewsets
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (
    UserSerializer, UserUpdateSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

import datetime, secrets, requests, re

User = get_user_model()

class CustomLoginView(APIView):
    permission_classes = []

    def post(self, request):
        login = request.data.get("login")
        password = request.data.get("password")

        if re.match(r"[^@]+@[^@]+\.[^@]+", login):
            kwargs = {'email': login}
        else:
            kwargs = {'username': login}

        user = authenticate(request, password=password, **kwargs)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"detail": "Неверные учетные данные"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class YandexSocialAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        code = request.data.get("code")
        redirect_uri = request.data.get("redirect_uri")
        if not code or not redirect_uri:
            return Response({"detail": "Нет кода или redirect_uri"}, status=400)

        # Получаем client_id/secret из settings.py
        client_id = settings.SOCIALACCOUNT_PROVIDERS['yandex']['APP']['client_id']
        client_secret = settings.SOCIALACCOUNT_PROVIDERS['yandex']['APP']['secret']

        # 1. Меняем code на access_token Яндекса
        try:
            token_resp = requests.post(
                "https://oauth.yandex.ru/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
            token_resp.raise_for_status()
            ya_access_token = token_resp.json()["access_token"]
        except Exception as e:
            return Response({"detail": f"Ошибка при получении access_token: {str(e)}"}, status=400)

        try:
            profile_resp = requests.get(
                "https://login.yandex.ru/info",
                params={"format": "json"},
                headers={"Authorization": f"OAuth {ya_access_token}"},
                timeout=10,
            )
            profile_resp.raise_for_status()
            profile = profile_resp.json()
        except Exception as e:
            return Response({"detail": f"Ошибка при получении профиля: {str(e)}"}, status=400)

        email = profile.get('default_email') or (profile.get('emails') or [None])[0]
        if not email:
            return Response({"detail": "Не удалось получить email из профиля Яндекса"}, status=400)

        user, _ = User.objects.get_or_create(email=email, defaults={
            "username": email.split('@')[0],
            "is_active": True,
        })

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

# @method_decorator(csrf_exempt, name='dispatch')
# class ProxyYandexSocialAuth(APIView):
#     def post(self, request: Request):
#         # Просто пробрасывает все данные на стандартный djoser endpoint
#         backend_url = "http://localhost:8000/api/auth/o/yandex-oauth2/"
#         r = requests.post(backend_url, json=request.data)
#         return Response(r.json(), status=r.status_code)

class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer  # Используем UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(email=serializer.validated_data['email']).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = user.pk
            send_mail(
                'Сброс пароля',
                f'Перейдите по ссылке: http://localhost:8000/reset-password/confirm?uid={uid}&token={token}',
                'noreply@teammate.com',
                [user.email]
            )
        return Response({'detail': 'Если email найден — письмо отправлено.'})

class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.get(pk=serializer.validated_data['uid'])
            if default_token_generator.check_token(user, serializer.validated_data['token']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'detail': 'Пароль изменён.'})
            else:
                return Response({'detail': 'Неверный токен.'}, status=400)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=404)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# class SetupOTPView(LoginRequiredMixin, AllAuthActivateTOTPView):
#     template_name = 'account/mfa/otp_qr.html'
#     success_url = reverse_lazy('verify_otp')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         totp_uri = self.get_totp_uri()
#         img = qrcode.make(totp_uri)
#         buffer = io.BytesIO()
#         img.save(buffer, format="PNG")
#         context['qr_code'] = base64.b64encode(buffer.getvalue()).decode()
#         context['secret_key'] = self.get_secret_key()
#         return context
#
# class VerifyOTPView(LoginRequiredMixin, AllAuthAuthenticateView):
#     template_name = 'account/mfa/otp_auth.html'
#     success_url = reverse_lazy('profile')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Активируем пользователя после успешной 2FA
#         self.request.user.is_active = True
#         self.request.user.save()
#         return response

# class CustomOTPLoginView(OTPLoginView):
#     form_class = OTPForm
#     template_name = 'account/otp_login.html'

# class TOTPSetupView(LoginRequiredMixin, TemplateView):
#     template_name = 'mfa/totp_setup.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         secret = generate_totp_secret()
#         totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
#             name=self.request.user.email or self.request.user.username,
#             issuer_name="Teammate"
#         )
#
#         img = qrcode.make(totp_uri)
#         buffer = io.BytesIO()
#         img.save(buffer, format="PNG")
#         qr_code = base64.b64encode(buffer.getvalue()).decode()
#
#         context.update({
#             'qr_code': qr_code,
#             'secret_key': secret_key,
#             'form': ActivateTOTPForm(initial={'secret': secret}),
#         })
#         return context

# class TOTPSetupView(AllAuthActivateTOTPView):
#     template_name = 'mfa/totp_setup.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Добавление QR-кода в контекст
#         totp_uri = pyotp.totp.TOTP(context['secret']).provisioning_uri(
#             name=self.request.user.email or self.request.user.username,
#             issuer_name="Your Site Name"
#         )
#         img = qrcode.make(totp_uri)
#         buffer = io.BytesIO()
#         img.save(buffer, format="PNG")
#         context['qr_code'] = base64.b64encode(buffer.getvalue()).decode()
#         return context

# class TOTPAuthenticateView(AllAuthAuthenticateView):
#     template_name = 'mfa/totp/auth.html'

# class UserTypeView(LoginRequiredMixin, TemplateView): # выбор типа пользователя больше не нужен, сущность "Заказчик" неактуальна
#     model = CustomUser
#     template_name = 'account/user_type.html'
#
#     def get(self, request, *args, **kwargs):
#         # if request.user.user_type != 'employee' and request.user.user_type != 'customer':
#         #     return render(request, self.template_name)
#         # return redirect('organizations_list')
#         if request.user.user_type:
#             return redirect('organizations:list')
#
#         return render(request, self.template_name)
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         user_type = request.POST.get('user_type')
#
#         #if user_type in ['employee', 'customer']:
#         if user_type in [choice[0] for choice in CustomUser.USER_TYPE_CHOICES]:
#             user.user_type = user_type
#             user.save()
#             return redirect('organizations:list')
#         else:
#             context = {'error_message': 'Неверный тип пользователя'}
#             return render(request, self.template_name, context)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #context['user_type_choices'] = self.request.user.USER_TYPE_CHOICES
#         context['user_type_choices'] = CustomUser.USER_TYPE_CHOICES
#         return context

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context