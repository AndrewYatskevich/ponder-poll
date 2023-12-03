from django.contrib.auth.views import LoginView
from django.urls import path
from users.views import SignUpView

urlpatterns = [
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path(
        "sign-in",
        LoginView.as_view(template_name="users/sign-in.html"),
        name="sign-in",
    ),
]
