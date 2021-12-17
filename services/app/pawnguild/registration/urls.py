from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("profile/update/", views.UpdateProfile.as_view(), name="update_profile"),
    path("confirm-account", views.ConfirmAccount.as_view(), name="confirm-account"),
]
