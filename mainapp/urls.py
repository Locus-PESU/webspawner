from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^guestpage/$', views.guestpage, name='guestpage'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^new_forum/$', views.new_forum, name='new_forum'),
    url(
        r'^profile_settings/$',
        views.profile_settings, name='profile_settings')
]
