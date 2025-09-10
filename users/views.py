import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config.settings import EMAIL_HOST_USER
from mailing_app.models import Mailing
from users.forms import CustomUserCreationForm, UserUpdateForm
from users.models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


User = get_user_model()


class ManagerUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    raise_exception = False
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()


class UserBlockToggleView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = False
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        messages.success(
            request,
            f"Пользователь {user.email} {'активирован' if user.is_active else 'заблокирован'}.",
        )
        return redirect("users:user_list")


class MailingToggleActiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = False
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()
        messages.success(
            request,
            f"Рассылка #{mailing.pk} теперь {'активна' if mailing.is_active else 'отключена'}.",
        )
        return redirect("mailing_app:mailing_list")


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Модель Детального просмотра пользователя.
    """

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:user_list")
        else:
            return reverse_lazy("mailing_app:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied

        # if not self.request.user.is_superuser:
        #     raise PermissionDenied
        # elif self.object.email == self.request.user.email:
        #     return self.object
        # return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse("users:detail", kwargs={"pk": self.object.pk})
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:user_list")
        else:
            return reverse_lazy("mailing_app:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied

        # if not self.request.user.is_superuser:
        #     raise PermissionDenied
        # return self.object
