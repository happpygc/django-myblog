# -*- coding: utf-8 -*-
'''
@date 2017-09-01 ����11:24:01 

@author: 
'''

from django.conf.urls import  url
from . import views
app_name = 'blog'
urlpatterns =[
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^index$', views.IndexView.as_view() ,name ='index' ),
    url(r'^post/(?P<pk>[0-9]+)/&',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^category/(?P<catepk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
# 评论
    url(r'^post_comment/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
    url(r'^about&',views.about,name='about'),
    url(r'^contact&',views.contact,name='contact')
    ]
