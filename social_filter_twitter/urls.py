from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin, auth

import app.urls

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'', include('social_django.urls', namespace = 'social')),
    url(r'', include(app.urls)),
]
