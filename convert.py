#!/usr/bin/env python
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
import sqlite3

from shorturl import models


conn = sqlite3.connect('prod.sql3')
c = conn.cursor()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    k, _ = models.User.objects.get_or_create(username="kimvais",
                                             email="kimvais@gmail.com")
    k.save()
    for pk, addr, clicks in c.execute('SELECT * FROM urls'):
        u = models.URL.objects.create(id=pk, url=addr, clicks=clicks,
                                      owner=None)
        logger.info("Converting #{0} {1}".format(pk, addr))
        u.save()
    # for i in range(utils.utoi('100')):
    #     u, created = models.URL.objects.get_or_create(id=i, defaults=dict(
    #         url=None,
    #         clicks=0,
    #         owner=k))
    #     if not created:
    #         continue
    #     logger.info("Creating placeholder #{0}".format(i))
    #     u.save()


if __name__ == '__main__':
    main()
