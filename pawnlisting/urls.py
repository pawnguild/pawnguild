from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.list_pawn, name='list_pawn'),
    path('list', views.list_pawn, name='list_pawn'),
    path('add_pawn', views.PawnForm.as_view(), name="add_pawn"),
    #path(pawn/12)
]
