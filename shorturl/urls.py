from django.conf.urls import patterns, include, url
from shorturl.views import about, home, redirector

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", home, name="home"),
    url(r"about", about, name="about"),
    url(r"^(.*)$", redirector, name="redirector")
)
