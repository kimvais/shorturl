from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from shorturl import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", views.Home.as_view(), name="home"),
    url(r"about[/]?$", views.About.as_view(), name="about"),
    url(r'log[/]?$', login_required(views.URLLog.as_view()), name="log"),
    url(r'login[/]?$', views.Login.as_view(), name="login"),
    url(r'logout[/]?$', views.Logout.as_view(), name="logout"),
    url(r'shorten', views.Home.as_view(), name="shorten"),
    url(r'', include('social_auth.urls')),
    url(r"^!/(?P<short>.*)$", views.Results.as_view(), name="results"),
    url(r"^(?P<short>.*)$", views.Redirect.as_view(), name="redirector")
)
