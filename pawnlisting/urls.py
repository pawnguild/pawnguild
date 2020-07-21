from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.SteamPawnList.as_view(), name='list-steam-pawns'),
    path('pawn_list/steam', views.SteamPawnList.as_view(), name='list-steam-pawns'),
    path('pawn_list/switch', views.SwitchPawnList.as_view(), name='list-switch-pawns'),

    path('pawn/steam/<pk>/', views.SteamPawnDetail.as_view(), name="view-steam-pawn"),
    path('pawn/switch/<pk>/', views.SwitchPawnDetail.as_view(), name="view-switch-pawn"),

    path('pawn/<pk>/update/', views.PawnUpdate.as_view(), name="update_pawn"),
    path('pawn/<pk>/delete/', views.PawnDelete.as_view(), name="delete_pawn"),
    path("manage_pawns", views.PawnManager.as_view(), name="manage_pawns"),
    path("api/pawns", api.PawnAPIList.as_view(), name="api_pawn_list"),

    path("profile/update/", views.UpdateProfile.as_view(), name="update_profile"),
    path("add_pawn/select_platform", views.ChoosePawnPlatform.as_view(), name="select_platform"),
    path("add_pawn/steam/", views.CreateSteamPawn.as_view(), name="create-steam-pawn"),
    path("add_pawn/switch/", views.CreateSwitchPawn.as_view(), name="create-switch-pawn"),
]