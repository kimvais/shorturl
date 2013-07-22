import logging
import sqlite3

from shorturl import models, utils


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
