from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("players/", views.players, name="players"),
    path("players/<slug:slug>/", views.player_detail, name="player_detail"),
    path("matches/", views.matches, name="matches"),
    path("news/", views.news, name="news"),
    path("news/<slug:slug>/", views.article_detail, name="article_detail"),
    path("history/", views.history, name="history"),
    path("standings/", views.standings, name="standings"),
    path("contact/", views.contact, name="contact"),
]
