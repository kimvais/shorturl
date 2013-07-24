setup:
	@rm short_urls.sqlite3
	@python manage.py syncdb
	@python manage.py migrate shorturl
	@python manage.py migrate social_auth
	@python convert.py
