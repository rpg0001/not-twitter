from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm


@login_required
def profile(request):
    # TODO: get user tweets as context
    return render(request, 'users/profile.html', {'title': 'Profile', 'tweets': { "tweet": "hello"}})

@login_required
def profile_likes(request):
    # TODO: get user likes as context
    return render(request, 'users/profile.html', {'title': 'Profile', 'likes': {}})

@login_required
def profile_comments(request):
    # TODO: get user comments as context
    return render(request, 'users/profile.html', {'title': 'Profile', 'comments': {}})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('signin')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'title': "Sign up", 'form': form})


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully!")
            return redirect("/")
        else:
            messages.error(request, "Incorrect username or password")
            return redirect("signin")

    else:
        return render(request, 'users/signin.html', {'title': 'Sign in'})

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect("/")


@login_required
def settings(request):
    if request.method == 'POST':
        # user_form = UserUpdateForm(request.POST, instance=request.user)
        # user_form.is_valid() and
        # user_form.save()
        # user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'There was an error updating your profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'title': 'Settings', 'profile_form': profile_form}
    return render(request, 'users/settings.html', context)
