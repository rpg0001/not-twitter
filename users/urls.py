from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('profile/likes', views.profile, name='profile_likes'),
    path('profile/comments', views.profile, name='profile_comments'),
    path('profile/retweets', views.profile, name='profile_retweets'),
    path('settings/', views.settings, name='settings')
]