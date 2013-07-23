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
from urlparse import urlunparse, urlparse

from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, View, FormView, DetailView

from models import URL, get_free_id
from shorturl import forms
from utils import itou, utoi


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

    def form_valid(self, form):
        url = form.cleaned_data['url']
        seen = URL.objects.filter(url=url)
        if len(seen) > 0:
            su = seen[0]
        else:
            n = get_free_id()
            su = URL.objects.create(id=n, url=url, clicks=0)
        self.pk = su.id
        self.short = itou(su.id)
        self.url = su.url
        return super(Home, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        hosturl = self.request.build_absolute_uri()
        if self.pk is not None:
            short = hosturl + self.short
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
        abs_url = self.request.build_absolute_uri()
        ctx['short'] = '{1}://{2}/{0}'.format(self.object.short,
                                                   *urlparse(abs_url)[:2])
        return ctx
