from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import ProUser
from .forms import ProUserForm


def register(request):
    if request.method == 'POST':
        form = ProUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = ProUserForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProUserForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your account was deleted successfully!')
    return redirect('register')


