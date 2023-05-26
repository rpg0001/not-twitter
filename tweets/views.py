
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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


@login_required
def index(request):
    # TODO: incorporate retweets into feeds
    tweets = Tweet.objects.all()
    return render(request, 'tweets/tweets.html', {"title": "Home", "tweets": tweets})


@login_required
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
        return redirect("/")
    else:
        return redirect("/")

@login_required
def like(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        already_liked = liked(request.user, tweet)

        if not already_liked:
            tweet.likes.add(request.user)

        if already_liked:
            tweet.likes.remove(request.user)

        return redirect(request.POST['path'])
    else:
        return redirect("/")

@login_required
def comment(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comment = Comment(tweet=tweet, text=request.POST["text"], user=request.user)
        comment.save()
        return redirect(request.POST["path"])
    else:
        return redirect("/")


@login_required
def retweet(request, tweet_id):
    if request.method == "POST":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        retweet = Retweet(tweet=tweet, user=request.user)
        retweet.save()
        return redirect(request.POST["path"])
    else:
        return redirect("profile")


@login_required
def following(request):
    followed_users = request.user.profile.following.all()
    tweets = Tweet.objects.filter(user__in=followed_users)
    return render(request, 'tweets/following.html', {"title": "Following", "tweets": tweets})


@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
        if tweet.user.id == request.user.id:
            tweet.delete()
            print("deleted tweet")
            return redirect(request.POST['path'])
        print("not your tweet")
        return redirect(request.POST['path'])
    else:
        print("wrong method")
        return redirect('/')
