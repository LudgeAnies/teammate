import pytest
import pyotp
from users.models import CustomUser
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator

@pytest.mark.django_db
def test_user_registration_and_email_confirm(client):
    resp = client.post('/api/auth/users/', {
        "email": "user1@example.com",
        "username": "user1",
        "first_name": "Иван",
        "last_name": "Иванов",
        "password": "Ks5#Mz4#Pw4%",
        "re_password": "Ks5#Mz4#Pw4%"
    })
    assert resp.status_code == 201
    user = CustomUser.objects.get(email="user1@example.com")
    assert not user.is_active

    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    resp2 = client.post('/api/auth/users/activation/', {"uid": uid, "token": token})
    assert resp2.status_code in (200, 204)
    user.refresh_from_db()
    assert user.is_active

@pytest.mark.django_db
def test_otp_setup_and_login(client):
    user = CustomUser.objects.create_user(
        username="user2", email="user2@ex.com", first_name="Алексей", last_name="Алексеев",
        password="Ks5#Mz4#Pw4%", is_active=True
    )
    client.force_authenticate(user)
    resp = client.get('/api/users/otp/setup/')
    assert resp.status_code == 200
    secret = resp.json()['secret']
    assert len(secret) > 10

    user.otp_secret = secret
    user.save()
    client.logout()

    resp = client.post('/api/users/login/', {"username": "user2", "password": "Ks5#Mz4#Pw4%"})
    assert resp.status_code == 200
    temp_token = resp.json()['temp_token']

    otp_code = pyotp.TOTP(secret).now()
    resp2 = client.post('/api/users/otp/verify', {"temp_token": temp_token, "otp": otp_code})
    assert resp2.status_code == 200
    assert 'access_token' in resp2.json()


# import pytest
# import pyotp
# from django.urls import reverse
# from rest_framework.test import APIClient
# from users.models import CustomUser
# from djoser.utils import encode_uid
# # from djoser.tokens import activation_token
# from django.contrib.auth.tokens import default_token_generator
#
# @pytest.mark.django_db
# def test_registration_and_email_confirmation():
#     client = APIClient()
#     # 1. Регистрация
#     data = {
#         "email": "test1@example.com",
#         "username": "testuser1",
#         "first_name": "Тест",
#         "last_name": "Юзер",
#         "password": "Ks5#Mz4#Pw4%It6#Sr1@",
#         "re_password": "Ks5#Mz4#Pw4%It6#Sr1@",
#     }
#     response = client.post("/api/auth/users/", data)
#     print(response.json())
#     assert response.status_code == 201
#
#     # 2. Пользователь создан, но не активен
#     user = CustomUser.objects.get(email="test1@example.com")
#     assert not user.is_active
#
#     # 3. Имитация подтверждения email
#     uid = encode_uid(user.pk)
#     # token = activation_token.make_token(user)
#     token = default_token_generator.make_token(user)
#     response = client.post("/api/auth/users/activation/", {"uid": uid, "token": token})
#     print(response.json())
#     assert response.status_code in [200, 204]
#
#     # 4. Пользователь теперь активен
#     user.refresh_from_db()
#     assert user.is_active
#
# @pytest.mark.django_db
# def test_login_and_otp_flow():
#     client = APIClient()
#     user = CustomUser.objects.create_user(
#         username="otpuser",
#         email="otp@example.com",
#         password="Qwerty123!",
#         is_active=True,
#         otp_secret="JBSWY3DPEHPK3PXP"
#     )
#     # 1. Логин, шаг 1
#     response = client.post("/api/users/login/", {
#         "username": "otpuser",
#         "password": "Qwerty123!",
#     })
#     assert response.status_code == 200
#     temp_token = response.json()["temp_token"]
#
#     # 2. Логин, шаг 2 (OTP)
#     otp_code = pyotp.TOTP(user.otp_secret).now()
#     response = client.post("/api/users/auth/otp/verify", {
#         "temp_token": temp_token,
#         "otp": otp_code,
#     })
#     assert response.status_code == 200
#     assert "access_token" in response.json()
