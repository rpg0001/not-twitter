from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'My Profile'})


def profile_public(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    already_following = False
    for follower in user.profile.followers.all():
        if follower.id == request.user.id:
            already_following = True

    return render(request, 'users/profile_public.html',
                  {'title': 'Profile', 'user_p': user, 'already_following': already_following})


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
    return redirect("signin")


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


def follow(request, user_id):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, pk=user_id)
        already_following = False

        for followed_user in request.user.profile.following.all():
            if followed_user == user_to_follow:
                already_following = True
                break

        if not already_following:
            request.user.profile.following.add(user_to_follow)
            user_to_follow.profile.followers.add(request.user)

        if already_following:
            request.user.profile.following.remove(user_to_follow)
            user_to_follow.profile.followers.remove(request.user)

    return redirect(request.POST['path'])


def followers(request, user_id):
    user_p = get_object_or_404(User, pk=user_id)
    followers = user_p.profile.followers.all()
    return render(request, 'users/users_list.html', {'title': 'Followers', 'user_list': followers, 'user_p': user_p})


def following(request, user_id):
    user_p = get_object_or_404(User, pk=user_id)
    following = user_p.profile.following.all()
    return render(request, 'users/users_list.html', {'title': 'Following', 'user_list': following, 'user_p': user_p})
