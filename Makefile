setup:
	@rm short_urls.sqlite3
	@python manage.py syncdb
	@python manage.py migrate shorturl
	@python convert.py
