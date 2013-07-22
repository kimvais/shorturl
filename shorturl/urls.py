from django.conf.urls import patterns, include, url
from shorturl.views import Home, About, Redirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", Home.as_view(), name="home"),
    url(r"about", About.as_view(), name="about"),
    url(r"^(?P<short>.*)$", Redirect.as_view(), name="redirector")
)
