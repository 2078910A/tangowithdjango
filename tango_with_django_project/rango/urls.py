from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       #ex: /rango/
                       url(r'^$', views.index, name='index'),
                       #ex: /rango/about/
                       url(r'^about/', views.about, name='about'),
                       #ex: /rango/add_category
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       #ex: /rango/category/other-frameworks/
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
                           views.category, name='category'),
                       #ex: /rango/category/python/add_page/
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
                       views.add_page, name='add_page'),
                       #ex: /rango/register/
                       url(r'^register/$', views.register, name='register'),
                       #ex: /rango/login/
                       url(r'^login/$', views.user_login, name='login'),
                       #ex: /rango/restricted/
                       url(r'^restricted/', views.restricted, name='restricted'),
                       #ex: /rango/logout/
                       url(r'^logout/$', views.user_logout, name='logout'),
                       )