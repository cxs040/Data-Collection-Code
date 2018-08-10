from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout


from . import views

urlpatterns = [
               url(r'^login/$', auth_views.login, name='login'),
               url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
               url(r'^signup/$', views.signup, name='signup'),
               url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
               url(r'^update/$', views.update_profile, name='update_profile'),
               url(r'^home/$', views.home, name='home'),
               url(r'^path/$', views.path, name='path'),
               url(r'^programming/$', views.programming, name='programming'),
               url(r'^logoutandthankyou/$', auth_views.logout, {'next_page': '/thankyou'}, name='logoutandthankyou'),
               url(r'^thankyou/$', views.thankyou, name='thankyou'),
               url(r'^manage/$', views.manage, name='manage'),
               url(r'^manage/(?P<report_id>[0-9]+)/$', views.report, name='report'),
               url(r'^manage/(?P<report_id>[0-9]+)/user/(?P<user_id>[0-9]+)$', views.personalReport, name='personalReport'),
               ]
