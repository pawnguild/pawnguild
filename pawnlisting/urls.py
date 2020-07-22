from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.SteamPawnList.as_view(), name='list-all-pawns'),
    path('pawn_list/all', views.ListAllPawns.as_view(), name='list-all-pawns'),
    path('pawn_list/steam', views.SteamPawnList.as_view(), name='list-steam-pawns'),
    path('pawn_list/switch', views.SwitchPawnList.as_view(), name='list-switch-pawns'),

    path('pawn/steam/<pk>/', views.SteamPawnDetail.as_view(), name="view-steam-pawn"),
    path('pawn/switch/<pk>/', views.SwitchPawnDetail.as_view(), name="view-switch-pawn"),

    path("add_pawn/select_platform", views.ChoosePawnPlatform.as_view(), name="select_platform"),
    path("add_pawn/steam/", views.CreateSteamPawn.as_view(), name="create-steam-pawn"),
    path("add_pawn/switch/", views.CreateSwitchPawn.as_view(), name="create-switch-pawn"),

    path('pawn/steam/<pk>/update/', views.SteamPawnUpdate.as_view(), name="update-steam-pawn"),
    path('pawn/switch/<pk>/update/', views.SwitchPawnUpdate.as_view(), name="update-switch-pawn"),

    path('pawn/steam/<pk>/delete/', views.SteamPawnDelete.as_view(), name="delete-steam-pawn"),
    path('pawn/switch/<pk>/delete/', views.SwitchPawnDelete.as_view(), name="delete-switch-pawn"),

    path("manage_pawns", views.PawnManager.as_view(), name="manage_pawns"),
    path("api/pawns", api.PawnAPIList.as_view(), name="api_pawn_list"),

    path("profile/update/", views.UpdateProfile.as_view(), name="update_profile"),

]