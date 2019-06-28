from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm, ProfileImage, UserUpdateForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_rest(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'username': user.username,
        'avatar': user.profile.img.url

        },
        status=HTTP_200_OK)


# @api_view(["POST"])
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# def create_auth(request):
    # print(request)
    # serialized = UserCreate(data=request.data)
    # if serialized.is_valid():
    #     User.objects.create_user(**serialized.init_data)
    #     return Response(serialized.data, status=HTTP_201_CREATED)
    # else:
    #     return Response(serialized._errors, status=HTTP_400_BAD_REQUEST)


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
