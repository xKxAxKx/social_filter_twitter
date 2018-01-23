## これは何か
社会性フィルターが実装されたTwitterクライアントです

## 社会性フィルターとは何か
これです
https://twitter.com/sh4869sh/status/767244989503901696

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
