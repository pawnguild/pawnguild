from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.PawnList.as_view(), name='list_pawn'),
    path('list/', views.PawnList.as_view(), name='list_pawn'),
    path('add_pawn/', views.PawnCreate.as_view(), name="create_pawn"),
    path('pawn/<pk>/', views.PawnDetail.as_view(), name="view_pawn"),
    path('pawn/<pk>/update/', views.PawnUpdate.as_view(), name="update_pawn"),
    path('pawn/<pk>/delete/', views.PawnDelete.as_view(), name="delete_pawn"),
    path("manage_pawns", views.PawnManager.as_view(), name="manage_pawns"),
    path("api/pawns", api.PawnAPIList.as_view(), name="api_pawn_list"),
    path("profile/update/", views.UpdateProfile.as_view(), name="update_profile"),
]