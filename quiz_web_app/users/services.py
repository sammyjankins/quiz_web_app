from .forms import UserRegisterForm
from django.contrib import messages


def register_user(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, f'Аккаунт успешно зарегистрирован! Войдите чтобы продолжить работу.')
    return form
