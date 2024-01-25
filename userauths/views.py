from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import (
    UserRegisterForm, UserLoginForm,
    UserUpdateForm, ProfileUpdateForm)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"The account for {username} was created successfully.")
            return redirect("blog:home")
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/signup.html", context)


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:home")
    else:
        form = UserLoginForm()
    context = {
        "form": form
    }
    return render(request, "userauths/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("userauths:login")


def profile(request):
    user = request.user
    if request.method == "POST":
        u_form =  UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("userauths:profile")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "userauths/profile.html", context)
