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

import string
from urlparse import urlparse, urlunparse
import requests

CHARSET = string.digits + string.ascii_letters + "$-_.+!*"
BASE = len(CHARSET)
L = 4


def itou(i):
    digits = tobase(BASE, i)
    u = [CHARSET[int(x)] for x in digits]
    return "".join(u)


def utoi(u):
    u = list(u)
    u.reverse()
    i = 0
    for pos in range(0, len(u)):
        i += BASE ** pos * CHARSET.find(u[pos])
    return int(i)


def tobase(base, number):
    global tb

    def tb(b, n, result=[]):
        if n == 0:
            return result
        else:
            return tb(b, n / b, [str(n % b)] + result)

    if not isinstance(base, int):
        raise TypeError, 'invalid base for tobase()'
    if base <= 0:
        raise ValueError, 'invalid base for tobase(): %s' % base
    if (not isinstance(number, int)) and (not isinstance(number, long)):
        raise TypeError, 'tobase() of non-integer'
    if number == 0:
        return '0'
    if number > 0:
        return tb(base, number)
    if number < 0:
        return '-' + tb(base, -1 * number)

def base_template_variables(request):
    return dict(
        SITENAME='77.fi',
        AUTHOR_NICK='kimvais',
        AUTHOR_NAME="Kimmo Parviainen-Jalanko",
        COPYRIGHTYEAR='2009-2013',
    )

def get_real_url(raw_url, timeout=3.0):
    parsed = urlparse(raw_url)
    if not parsed.scheme:
        parsed = urlparse("http://" + raw_url)
    url = urlunparse(parsed)
    try:
        r = requests.get(url, timeout=timeout)
        return r.url
    except requests.RequestException:
        return url