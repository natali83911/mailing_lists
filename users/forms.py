from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.urls import reverse_lazy

from mailing_app.forms import StyleFormMixin

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    email = forms.EmailField(label="Email", required=True)


class UserUpdateForm(StyleFormMixin, ModelForm):
    """
    Модель изменение пользователя.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "country",
            # "is_active",
            # "is_superuser",
            # "is_staff",
            "avatar",
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
        }
        success_url = reverse_lazy("users:users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields["phone_number"].widget

        self.fields["password"].widget = forms.HiddenInput()
        phone_number.attrs["class"] = "form-control bfh-phone"
        phone_number.attrs["data-format"] = "+7 (ddd) ddd-dd-dd"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует.")

        return email
