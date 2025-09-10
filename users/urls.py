from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users.views import RegisterView, email_verification
from users.views import (
    ManagerUserListView,
    UserBlockToggleView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("users/", ManagerUserListView.as_view(), name="user_list"),
    path(
        "users/<int:pk>/block-toggle/",
        UserBlockToggleView.as_view(),
        name="user_block_toggle",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/registration/password_reset_form.html",
            email_template_name="users/registration/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/registration/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
