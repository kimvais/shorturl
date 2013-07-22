# Create your views here.
from pprint import pprint

from django.http import HttpResponseRedirect, Http404
from django.db.models import Max
from django.views.generic import TemplateView, View

from models import URL
from utils import itou, utoi


class Home(TemplateView):
    def post(self, _):
        c = super(Home, self).get_context_data()
        url = self.request.POST['url']
        seen = URL.objects.filter(url=url)
        if len(seen) > 0:
            su = seen[0]
        else:
            n = URL.objects.all().aggregate(Max("id"))['id__max'] + 1
            su = URL.objects.create(id=n, url=url, clicks=0)
        pprint(su)
        c['short'] = "http://77.fi/" + itou(su.id)
        c['url'] = su.url
        return self.render_to_response(c)

    def get_template_names(self):
        if self.request.method == "POST":
            return 'results.html'
        else:
            return 'home.html'


class About(TemplateView):
    template_name = 'about.html'


class Redirect(View):
    def dispatch(self, request, *args, **kwargs):
        self.short = kwargs.pop('short')
        return super(Redirect, self).dispatch(request, *args, **kwargs)

    def get(self, _):
        urlid = utoi(self.short)
        try:
            shorturl = URL.objects.filter(id=urlid)[0]
            shorturl.clicks += 1
        except (KeyError, IndexError) as e:
            raise Http404("%s not in database" % self.short)
        return HttpResponseRedirect(shorturl.url)

