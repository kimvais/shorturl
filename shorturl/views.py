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
import logging
from urlparse import urlparse

from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, View, FormView, DetailView, ListView

from models import URL
from shorturl import forms, settings
from shorturl.models import get_free_id
from utils import itou, utoi

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Home(FormView):
    template_name = "home.html"
    form_class = forms.URLShortenForm

    def dispatch(self, request, *args, **kwargs):
        self.url = request.get_full_path()
        self.pk = None
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.pk is not None:
            return '/!/{0}'.format(self.short)
        else:
            return '/'

    def get(self, request, *args, **kwargs):
        if 'url' in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super(Home, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(Home, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        url = form.cleaned_data['url']
        seen = URL.objects.filter(url=url)
        if len(seen) > 0:
            su = seen[0]
        else:
            n = get_free_id()
            su = URL.objects.create(id=n, url=url, clicks=0)
            logger.debug(self.request.user)
            if self.request.user.is_authenticated():
                su.owner = self.request.user
                su.save()
        self.pk = su.id
        self.short = itou(su.id)
        self.url = su.url
        return super(Home, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        if self.pk is not None:
            short = settings.BASEURL + self.short
        else:
            short = None
        ctx.update(dict(url=self.url, short=short))
        return ctx


class About(TemplateView):
    template_name = 'about.html'


class Redirect(View):
    def dispatch(self, request, *args, **kwargs):
        self.short = kwargs.pop('short')
        return super(Redirect, self).dispatch(request, *args, **kwargs)

    def get(self, _):
        urlid = utoi(self.short)
        try:
            shorturl = URL.objects.get(id=urlid)
            shorturl.clicks += 1
            shorturl.save()
        except (URL.DoesNotExist, OverflowError):
            # OverflowError is odd, see
            raise Http404("%s not in database" % self.short)
        return HttpResponseRedirect(shorturl.url)


class Results(DetailView):
    template_name = 'results.html'
    model = URL

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.pk)

    def dispatch(self, request, *args, **kwargs):
        self.pk = utoi(kwargs.pop('short'))
        return super(Results, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(Results, self).get_context_data(**kwargs)
        short = '{0}{1}'.format(settings.BASEURL, self.object.short)
        ctx['short'] = short
        ctx['savings'] = len(self.object.url) - len(short)

        return ctx


class URLLog(ListView):
    template_name = "log.html"
    model = URL


class Login(TemplateView):
    template_name = "login_provider.html"


