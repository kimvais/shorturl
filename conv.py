import sqlite3
import logging

from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError

from shorturl.utils import itou


logger = logging.getLogger(__name__)


def main():
    c = sqlite3.connect('short_urls.sqlite3').cursor()
    c.execute('SELECT id, url, clicks, created FROM shorturl_url')
    try:
        urls = Table.create('short_urls', schema=[HashKey('url_id'), ])
    except JSONResponseError:
        urls = Table('short_urls')

    keys = list()
    for row in c.fetchall():
        num_id, url, clicks, created = row
        logger.info('ID: {}({}) {} / {} ({})'.format(itou(num_id), num_id, url, clicks, created))
        key = itou(num_id)
        keys.append(num_id)
        uo = Item(urls, data=dict(url_id=key, id_n=num_id, url=url, clicks=clicks, created=created))
        uo.save(overwrite=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
