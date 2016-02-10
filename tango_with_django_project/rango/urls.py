from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       #ex: /rango/
                       url(r'^about/', views.about, name='about'),
                       #ex: /rango/about/
                       url(r'^category/(?P<category_name_url>[\w\-]+)/$',
                           views.category, name='category'),
                       #ex: /rango/category/other-frameworks/
                       )

