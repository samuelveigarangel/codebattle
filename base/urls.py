from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("event/<int:pk>/", views.event_page, name="event")
]
