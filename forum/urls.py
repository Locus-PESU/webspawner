from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(\w+)/$', views.index, name='index'),
    url(r'^board/([0-9]+)/([0-9]+)/$', views.board, name='board'),
    url(r'^thread/([0-9]+)/([0-9]+)/$', views.thread, name='thread'),
    url(r'^add_thread/([0-9]+)/$', views.add_thread, name='add_thread'),
    url(r'^add_post/([0-9]+)/$', views.add_post, name='add_post'),
    url(r'^display_user/([0-9]+)/([0-9]+)/$', views.display_user,
        name='display_user'),
    url(r'^upload_new_thread/([0-9]+)/$', views.upload_new_thread,
        name='upload_new_thread'),
    url(r'^upload_new_post/([0-9]+)/$', views.upload_new_post,
        name='upload_new_post'),
    url(r'^add_rating/([0-9]+)/$', views.add_rating, name='add_rating'),
    url(r'^send_dm/([0-9]+)/$', views.send_dm, name='send_dm'),
    url(r'^search/$', views.search, name='search')
]
