from pprint import pprint

from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, View

from models import URL, get_free_id
from utils import itou, utoi


class Home(TemplateView):
    def post(self, request):
        ctx = super(Home, self).get_context_data()
        url = request.POST['url']
        seen = URL.objects.filter(url=url)
        if len(seen) > 0:
            su = seen[0]
        else:
            n = get_free_id()
            su = URL.objects.create(id=n, url=url, clicks=0)
        pprint(su)
        ctx['short'] = "http://77.fi/" + itou(su.id)
        ctx['url'] = su.url
        return self.render_to_response(ctx)

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

