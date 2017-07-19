from django.conf.urls import url
from django.conf import settings
from app import views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='logout')
]
