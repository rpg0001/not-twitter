from django import template
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Tweet, Comment


def index(request):
    tweets = Tweet.objects.order_by('-date')
    return render(request, 'tweets/index.html', {"title":"View all Tweets", "tweets": tweets})


def tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'tweets/detail.html', {"title": "View Tweet", "tweet": tweet})


def post(request):
    if request.method == "POST":
        new_tweet = Tweet(text=request.POST["text"])
        new_tweet.save()
        return HttpResponseRedirect("/tweets")
    else:
        return HttpResponseRedirect("/tweets")


def like(request, tweet_id):
    if request.method == "POST":
        liked_tweet = get_object_or_404(Tweet, pk=tweet_id)
        liked_tweet.likes = liked_tweet.likes + 1
        liked_tweet.save()
        print(request.POST["path"])
        return HttpResponseRedirect(request.POST["path"])
    else:
        return HttpResponseRedirect("/tweets")


def comment(request, tweet_id):
    if request.method == "POST":
        the_tweet = get_object_or_404(Tweet, pk=tweet_id)
        new_comment = Comment(tweet=the_tweet, text=request.POST["text"])
        new_comment.save()
        return HttpResponseRedirect(request.POST["path"])
    else:
        return HttpResponseRedirect("/tweets")
