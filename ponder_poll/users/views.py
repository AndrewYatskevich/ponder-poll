from django.views.generic import CreateView
from users.forms import SignUpForm
from users.models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    template_name = "users/sign-up.html"
    form_class = SignUpForm
    success_url = "users:sign-in"
