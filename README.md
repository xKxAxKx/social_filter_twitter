### NOTICE!
UNDER DEVELOPMENT

### Install package
```
$ pip install -r requirement.txt
```

### Run Django(Local)
```
$ python manage.py runserver --settings=social_filter_twitter.local_settings
```

### Run Djago(Prod)

```
$ python manage.py runserver 0.0.0.0:8000 --settings=social_filter_twitter.prod_settings
```

### RUN Django(Prod/Gunicorn)

```
$ gunicorn social_filter_twitter.wsgi --env DJANGO_SETTINGS_MODULE=social_filter_twitter.prod_settings --bind=0.0.0.0:8000
```
