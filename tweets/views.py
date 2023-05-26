from itertools import chain

from django import template
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Tweet, Comment, Retweet


# find out if the user has already liked a tweet
# call in like and tweet
def liked(user, tweet):
    liked = False

    for like in tweet.likes.all():
        if like == user:
            liked = True
            break

    return liked


def index(request):
    #tweets = Tweet.objects.all() | Retweet.objects.all()
    #tweets = list(chain(Tweet.objects.all(), Retweet.objects.all()))
    tweets = Tweet.objects.all()
    return render(request, 'tweets/tweets.html', {"title": "Home", "tweets": tweets})


def tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    already_liked = False
    if request.user.is_authenticated:
        already_liked = liked(request.user, tweet)

    return render(request, 'tweets/view_tweet.html', {"title": "View Tweet", "tweet": tweet, "already_liked": already_liked })

@login_required
def post(request):
    if request.method == "POST":
        tweet = Tweet(text=request.POST["text"], user=request.user)
        tweet.save()
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

@login_required
def like(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        already_liked = liked(request.user, tweet)

        if not already_liked:
            tweet.likes.add(request.user)

        if already_liked:
            tweet.likes.remove(request.user)

        return HttpResponseRedirect(request.POST['path'])
    else:
        return HttpResponseRedirect("/")

@login_required
def comment(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comment = Comment(tweet=tweet, text=request.POST["text"], user=request.user)
        comment.save()
        return HttpResponseRedirect(request.POST["path"])
    else:
        return HttpResponseRedirect("/")


@login_required
def retweet(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        retweet = Retweet(tweet=tweet, user=request.user)
        retweet.save()
        return HttpResponseRedirect(request.POST["path"])
    else:
        return HttpResponseRedirect("profile")


@login_required
def following(request):
    followed_users = request.user.profile.following.all()
    tweets = Tweet.objects.filter(user__in=followed_users)
    return render(request, 'tweets/following.html', {"title": "Following", "tweets": tweets})
