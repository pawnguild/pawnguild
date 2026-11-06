from django.urls import path, re_path
from django.views.generic import RedirectView, TemplateView

from . import views

urlpatterns = [
    path("password_reset/", views.PasswordRecover.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        TemplateView.as_view(template_name="password_reset/reset_sent.html"),
        name="password_reset_done",
    ),
    path("recover/", views.PasswordRecover.as_view(), name="password_reset_recover"),
    path(
        "recover/sent/",
        TemplateView.as_view(template_name="password_reset/reset_sent.html"),
        name="password_reset_sent",
    ),
    path(
        "recover/<str:signature>/",
        RedirectView.as_view(pattern_name="password_reset_sent"),
    ),
    path(
        "reset/done/",
        TemplateView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_complete",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordReset.as_view(),
        name="password_reset_reset",
    ),
    # Previously emailed add-on tokens need a fresh recovery request.
    re_path(
        r"^reset/[\w:-]+/$",
        TemplateView.as_view(template_name="password_reset/reset.html"),
    ),
    path("register/", views.Register.as_view(), name="register"),
    path("profile/update/", views.UpdateProfile.as_view(), name="update_profile"),
    path("confirm-account", views.ConfirmAccount.as_view(), name="confirm-account"),
]
