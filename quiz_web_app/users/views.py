from django.shortcuts import render
from .services import register_user
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


def register_view(request):
    if request.method == "POST":
        form = register_user(request)
        if form.is_valid():
            return redirect('login')
        else:
            form = UserRegisterForm(request.POST)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
