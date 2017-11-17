# coding:utf-8
from django.contrib import admin
from sign.models import *


# Register your models here.


class ConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'name', 'init_db', 'base_url', ]
    list_display_links = ('name', 'id')  # 显示链接
    search_fields = ['name']       # 搜索功能
    list_filter = ['status', 'init_db']


class EnvParamAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'type', 'mark', 'name', 'value', 'real_value']
    list_display_links = ('name', 'id')  # 显示链接
    search_fields = ['name']      # 搜索功能
    list_filter = ['status', 'type']     # 过滤器


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'name', 'is_init', 'result', 'msg']
    list_display_links = ('name', 'id')  # 显示链接
    search_fields = ['name']       # 搜索功能
    list_filter = ['status', 'result']


class GroupCaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'case', 'status']
    list_display_links = ('id',)  # 显示链接
    search_fields = ['case']       # 搜索功能
    list_filter = ['status', 'group']


class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'type', 'name',  'result']
    list_display_links = ('name', 'id')  # 显示链接
    search_fields = ['name']       # 搜索功能
    list_filter = ['status', 'result', 'type']


class CaseStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'case', 'step', 'status']
    list_display_links = ('id',)  # 显示链接
    search_fields = ['step']       # 搜索功能
    list_filter = ['status', 'case']


class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'name', 'result', 'msg']
    list_display_links = ('name', 'id')  # 显示链接
    search_fields = ['name']       # 搜索功能
    list_filter = ['status', 'result']


admin.site.register(Config, ConfigAdmin)
admin.site.register(EnvParam, EnvParamAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupCase, GroupCaseAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseStep, CaseStepAdmin)
admin.site.register(Step, StepAdmin)

# class PreVarGroupAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'status']
#     list_display_links = ('name', 'id')  # 显示链接
#     search_fields = ['name']       # 搜索功能
#     list_filter = ['status']                  # 过滤器

# class RequestInfoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'status', 'name', 'type', 'url']
#     list_display_links = ('name', 'id')  # 显示链接
#     search_fields = ['name']       # 搜索功能
#     list_filter = ['status', 'type']                  # 过滤器

# class StepPostProcessorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'step', 'postProcessor', 'status']
#     list_display_links = ('id',)  # 显示链接
#     search_fields = ['postProcessor']       # 搜索功能
#     list_filter = ['status', 'step']

# class PostProcessorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'status', 'name']
#     list_display_links = ('name', 'id')  # 显示链接
#     search_fields = ['name']    # 搜索功能
#     list_filter = ['status']

# admin.site.register(PreVarGroup, PreVarGroupAdmin)
# admin.site.register(RequestInfo, RequestInfoAdmin)
# admin.site.register(PostProcessor, PostProcessorAdmin)
# admin.site.register(StepPostProcessor, StepPostProcessorAdmin)
