"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sign import views, views_run, views_manage, views_search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^logout/$', views.logout),
    url(r'^login_action/$', views.login_action),
    url(r'^content_manage/$', views_manage.content_manage),
    url(r'^case_manage/(?P<group_id>\d+)/$', views_manage.case_manage),
    url(r'^group_manage/$', views_manage.group_manage),
    url(r'^group_manage/(?P<group_id>\d+)/$', views_manage.single_group_manage),
    url(r'^search_group/$', views_search.search_group),
    url(r'^group_case_manage/(?P<group_id>\d+)/$', views_manage.group_case_manage),
    url(r'^search_group_case/(?P<group_id>\d+)$', views_search.search_group_case),
    url(r'^case_manage/$', views_manage.case_manage),
    url(r'^search_case/$', views_search.search_case),
    url(r'^case_step_manage/(?P<group_id>\d+)/(?P<case_id>\d+)/$', views_manage.case_step_manage),
    url(r'^search_case_step/(?P<group_id>\d+)/(?P<case_id>\d+)$', views_search.search_case_step),
    url(r'^step_manage/$', views_manage.step_manage),
    url(r'^search_step/$', views_search.search_step),
    url(r'^whole_manage/$', views_manage.whole_manage),
    url(r'^run_group/(?P<group_id>\d+)/$', views_run.run_group),
    url(r'^copy_groups/$', views_run.copy_groups),
    url(r'^copy_group/$', views_run.copy_group),
    url(r'^copy_case/$', views_run.copy_case),
    url(r'^copy_manage/$', views_manage.copy_manage),
    url(r'^form_to_dict/$', views_run.change_form_to_dict),
    # url(r'^run_case/(?P<case_id>\d+)/$', views_run.run_case),
    url(r'^run_group_case/(?P<group_id>\d+)/(?P<case_id>\d+)/$', views_run.run_group_case),
    url(r'^run_whole_case/(?P<case_mode>[a-z]+)/$', views_run.run_whole_case),
    url(r'^accounts/login/$', views.index),
    url(r'^show_init_sql/$', views.show_init_sql),
    url(r'^show_app_log/$', views.show_app_log),
    url(r'^api/', include('sign.urls', namespace="sign")),
]
