# -*- coding: utf-8 -*-
#
# Copyright © 2009-2013 Kimmo Parviainen-Jalanko <k@77.fi>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


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

