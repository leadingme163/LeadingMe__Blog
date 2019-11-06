from django.urls import re_path

from blog import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^archive/$', views.archive, name='archive'),
    re_path('^tagCloud/$', views.tagCloud, name='tagCloud'),
    re_path('^notOpen/$', views.notOpen, name='notOpen'),
    re_path('^notAd/$', views.notAd, name='notOpen'),
    re_path('^blog_content/$', views.blog_content, name='blog_content'),
    re_path('^register/$', views.register, name='register'),
    re_path('^doRegister/$', views.doRegister, name='doRegister'),
    re_path('^login/$', views.login, name='login'),
    re_path('^out/$', views.out, name='out'),
    re_path('^relay/$', views.relay, name='relay'),
    re_path('^report/$', views.report, name='report')
]
