from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),
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
    path(
        "update-submission/<int:pk>/", views.update_submission, name="update-submission"
    ),
]
