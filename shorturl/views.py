# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db.models import Max
from models import Shorturl
from URLconvert import itou, utoi
from pprint import pprint


def home(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        url = request.POST['url']
        seen = Shorturl.objects.filter(url=url)
        if len(seen) > 0:
            su = seen[0]
        else:
            n = Shorturl.objects.all().aggregate(Max("id"))['id__max'] + 1
            su = Shorturl.objects.create(id=n, url=url, clicks=0)
        pprint(su)
        c['short'] = "http://77.fi/" + itou(su.id)
        c['url'] = su.url
        return render_to_response("results.html", c)
    else:
        return render_to_response("home.html", c)


def about(request):
    return render_to_response("about.html")


def redirector(request, short):
    urlid = utoi(short)
    try:
        shorturl = Shorturl.objects.filter(id=urlid)[0]
        shorturl.clicks += 1
    except (KeyError, IndexError) as e:
        return HttpResponse("%s not in database" % short)
    return HttpResponseRedirect(shorturl.url)

