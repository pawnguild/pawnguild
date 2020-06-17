from django.urls import path

from . import views

urlpatterns = [
    path('', views.PawnList.as_view(), name='list_pawn'),
    path('list/', views.PawnList.as_view(), name='list_pawn'),
    path('add_pawn/', views.PawnCreate.as_view(), name="create_pawn"),
    path('pawn/<pk>/', views.PawnDetail.as_view(), name="view_pawn"),
    path('pawn/<pk>/update/', views.PawnUpdate.as_view(), name="update_pawn"),
    path('pawn/<pk>/delete/', views.PawnDelete.as_view(), name="delete_pawn")
]