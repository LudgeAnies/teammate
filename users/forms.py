from allauth.account.forms import LoginForm, SignupForm
from django import forms
from .models import CustomUser
from django_otp.forms import OTPAuthenticationForm
#from django.contrib.auth.forms import PasswordResetForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class CustomLoginForm(LoginForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Объединяем поле ввода (email/username)
        self.fields['login'].label = "Email или имя пользователя"
        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email или username',
            'autofocus': 'autofocus',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль',
        })

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['login'].label = 'Имя пользователя или почта'

# class ContactForm(forms.Form):
#     name = forms.CharField(label='Ваше имя', max_length=100)
#     email = forms.EmailField(label='Email')
#     message = forms.CharField(label='Сообщение', widget=forms.Textarea)
#     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Фамилия'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field'})
        self.fields['email'].widget.attrs.update({'class': 'input-field'})
        self.fields['password1'].widget.attrs.update({'class': 'input-field'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field'})

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False  # Пользователь не активен до подтверждения 2FA
        user.save()
        return user


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for fieldname, field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class': 'input-field',
    #             'placeholder': field.label
    #         })
    #
    #     self.fields['first_name'] = forms.CharField(
    #         max_length=255,
    #         required=True,
    #         label='Имя',
    #         widget=forms.TextInput(attrs={'class': 'input-field'}),
    #     )
    #     self.fields['last_name'] = forms.CharField(
    #         max_length=255,
    #         required=True,
    #         label='Фамилия',
    #         widget=forms.TextInput(attrs={'class': 'input-field'}),
    #     )
    #     self.fields['captcha'] = ReCaptchaField(
    #         widget=ReCaptchaV2Checkbox(attrs={'class': 'recaptcha-field'})
    #     )

#     first_name = forms.CharField(
#         max_length=255,
#         required=True,
#         label=('Имя'),
#         widget=forms.TextInput(attrs={'class': 'input-field'}),
#     )
#     last_name = forms.CharField(
#         max_length=255,
#         required=True,
#         label=('Фамилия'),
#         widget=forms.TextInput(attrs={'class': 'input-field'}),
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for fieldname, field in self.fields.items():
#             field.widget.attrs.update({
#                 'class': 'input-field',
#                 'placeholder': field.label
#             })
#
#     captcha = ReCaptchaField(
#         widget=ReCaptchaV2Checkbox(attrs={'class': 'recaptcha-group'})
#     )

#     first_name = forms.CharField(
#         max_length=255,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'input-field',
#             'placeholder': 'Имя'
#         })
#     )
#     last_name = forms.CharField(
#         max_length=255,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'input-field',
#             'placeholder': 'Фамилия'
#         })
#     )
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].label = 'Имя'
#         self.fields['last_name'].label = 'Фамилия'


# class OTPForm(OTPAuthenticationForm): # не будет использоваться
#     otp_token = forms.CharField(
#         label='Одноразовый код из приложения',
#         widget=forms.TextInput(attrs={'autocomplete': 'off'}) # отключает автозаполнение
#     )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'avatar',
            'timezone',
        ]

# class CustomPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(
#         label="Email",
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email'})
#     )