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
from urlparse import urlparse, urlunparse
from django import forms
from django.conf import settings
import requests

logging.basicConfig()
logger = logging.getLogger(__name__)

if settings.DEBUG:
    logger.setLevel(logging.DEBUG)

class URLShortenForm(forms.Form):
    url = forms.CharField(max_length=2048)

    def clean_url(self):
        raw_url = self.cleaned_data['url']
        parsed = urlparse(raw_url)
        if not parsed.scheme:
            parsed = urlparse("http://" + raw_url)
        url = urlunparse(parsed)
        logger.debug(url)
        try:
            r = requests.get(url)
            return r.url
        except requests.RequestException:
            return url


