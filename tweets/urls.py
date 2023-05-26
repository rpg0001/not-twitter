from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tweets'),
    path('<int:tweet_id>/', views.tweet, name="tweet"),
    path('post/', views.post, name="post"),
    path('like/<int:tweet_id>/', views.like, name="like"),
    path('comment/<int:tweet_id>/', views.comment, name="comment"),
    path('retweet/<int:tweet_id>/', views.retweet, name="retweet"),
    path('following/', views.following, name='following_feed')
]
