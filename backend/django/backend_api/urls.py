from django.urls import path
from .views.users.login import LoginAPIView
from .views.users.logout import LogoutAPIView
from .views.users.signup import SignupAPIView

urlpatterns = [
    path("login", LoginAPIView.as_view()),
    path("signup", SignupAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
]
