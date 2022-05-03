from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("faq/", views.FAQ.as_view(), name="faq"),
]
