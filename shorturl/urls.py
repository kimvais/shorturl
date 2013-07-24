from django.conf.urls import patterns, include, url
from shorturl import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", views.Home.as_view(), name="home"),
    url(r"about", views.About.as_view(), name="about"),
    url(r'log', views.URLLog.as_view(), name="log"),
    url(r"^!/(?P<short>.*)$", views.Results.as_view(), name="results"),
    url(r"^(?P<short>.*)$", views.Redirect.as_view(), name="redirector")
)
