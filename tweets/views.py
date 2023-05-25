from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Tweet, Comment


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
    tweets = Tweet.objects.order_by('-date')
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
