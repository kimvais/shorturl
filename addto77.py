import logging
import click

from boto.dynamodb2.table import Table

logger = logging.getLogger(__name__)

@click.command()
@click.argument('url_id')
def main(url_id):
    urls = Table('short_urls')
    u = urls.get_item(url_id=url_id)
    u['clicks'] += 1
    u.save()
    logger.info(u['url'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
