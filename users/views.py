from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm, ProfileImage, UserUpdateForm


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('posts_list_url')
        else:
            form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})
    else:
        return redirect('profile')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('posts_list_url')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignInForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('posts_list_url')
                else:
                    print('User not found')
        else:
            form = SignInForm()
        return render(request, 'users/login.html', {'form': form})
    else:
        return redirect('profile')


@login_required
def profile(request):
    if request.method == "POST":
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if update_user.is_valid() and img_profile.is_valid():
            update_user.save()
            img_profile.save()
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'img_profile': img_profile,
        'update_user': update_user
    }
    return render(request, 'users/profile.html', data)
