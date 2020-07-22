from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.SteamPawnList.as_view(), name='list-all-pawns'),
    path('pawn_list/all',    views.ListAllPawns.as_view(),    name='list-all-pawns'),
    path('pawn_list/steam',  views.SteamPawnList.as_view(),   name='list-steam-pawns'),
    path('pawn_list/switch', views.SwitchPawnList.as_view(),  name='list-switch-pawns'),
    path('pawn_list/xbox1',  views.XboxOnePawnList.as_view(), name='list-xbox1-pawns'),
    path('pawn_list/ps4',    views.PS4PawnList.as_view(),     name="list-ps4-pawns"),
    path('pawn_list/ps3',    views.PS3PawnList.as_view(),     name="list-ps3-pawns"),

    path('pawn/steam/<pk>/',  views.SteamPawnDetail.as_view(),   name="view-steam-pawn"),
    path('pawn/switch/<pk>/', views.SwitchPawnDetail.as_view(),  name="view-switch-pawn"),
    path('pawn/xbox1/<pk>/',  views.XboxOnePawnDetail.as_view(), name="view-xbox1-pawn"),
    path('pawn/ps4/<pk>',     views.PS4PawnDetail.as_view(),     name="view-ps4-pawn"),
    path('pawn/ps3/<pk>',     views.PS3PawnDetail.as_view(),     name="view-ps3-pawn"),

    path("add_pawn/select_platform", views.ChoosePawnPlatform.as_view(), name="select_platform"),
    path("add_pawn/steam/",          views.CreateSteamPawn.as_view(),    name="create-steam-pawn"),
    path("add_pawn/switch/",         views.CreateSwitchPawn.as_view(),   name="create-switch-pawn"),
    path("add_pawn/xbox1/",          views.CreateXboxOnePawn.as_view(),  name="create-xbox1-pawn"),
    path("add_pawn/ps4/",            views.CreatePS4Pawn.as_view(),      name="create-ps4-pawn"),
    path("add_pawn/ps3/",            views.CreatePS3Pawn.as_view(),      name="create-ps3-pawn"),

    path('pawn/steam/<pk>/update/',  views.SteamPawnUpdate.as_view(),   name="update-steam-pawn"),
    path('pawn/switch/<pk>/update/', views.SwitchPawnUpdate.as_view(),  name="update-switch-pawn"),
    path('pawn/xbox1/<pk>/update/',  views.XboxOnePawnUpdate.as_view(), name="update-xbox1-pawn"),
    path('pawn/ps4/<pk>/update/',    views.PS4PawnUpdate.as_view(),     name="update-ps4-pawn"),
    path('pawn/ps3/<pk>/update/',    views.PS3PawnUpdate.as_view(),     name="update-ps3-pawn"),

    path('pawn/steam/<pk>/delete/',  views.SteamPawnDelete.as_view(),   name="delete-steam-pawn"),
    path('pawn/switch/<pk>/delete/', views.SwitchPawnDelete.as_view(),  name="delete-switch-pawn"),
    path('pawn/xbox1/<pk>/delete/',  views.XboxOnePawnDelete.as_view(), name="delete-xbox1-pawn"),
    path('pawn/ps4/<pk>/delete/',    views.PS4PawnDelete.as_view(),     name="delete-ps4-pawn"),
    path('pawn/ps3/<pk>/delete/',    views.PS3PawnDelete.as_view(),     name="delete-ps3-pawn"),


    path("manage_pawns", views.PawnManager.as_view(), name="manage_pawns"),
    path("api/pawns", api.PawnAPIList.as_view(), name="api_pawn_list"),

]