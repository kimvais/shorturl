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
"""
Usage: new77 [-uh] <short> <url>

    -u --update     Update an existing URL
    -h --help       Show help
"""
import logging
import docopt

from shorturl import utils, models

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main(opts):
    url = utils.get_real_url(opts['<url>'], timeout=5.0)
    pk = utils.utoi(opts['<short>'])
    update = opts.get('--update', False)
    logger.debug(opts)
    logger.debug(url)
    logger.debug(pk)
    try:
        su = models.URL.objects.get(pk=pk)
    except models.URL.DoesNotExist:
        su = models.URL.objects.create(pk=pk)
        su.url = url
        su.save()
    else:
        if update:
            su.url = url
            su.save()
        else:
            raise ValueError("Short url '{0}' exists!".format(su))


if __name__ == '__main__':
    main(docopt.docopt(__doc__))
