from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("user/<int:pk>/", views.user_page, name="profile"),
    path("event/<int:pk>/", views.event_page, name="event"),
    path(
        "registration-confirmation/<int:pk>/",
        views.registration_confirmation,
        name="registration-confirmation",
    ),
    path("account/", views.account_page, name="account"),
    path(
        "project-submission/<int:pk>/",
        views.project_submission,
        name="project-submission",
    ),
]
