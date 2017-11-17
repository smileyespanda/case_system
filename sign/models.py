# coding:utf-8
from django.db import models


# Create your models here.


class Config(models.Model):
    status = models.BooleanField(default=False)       # 只能允许一套环境是有效状态
    auto_tag = models.BooleanField(default=True)      # 是否需要开启自动启用/禁用当前环境的相关用例
    init_db = models.BooleanField(default=False)      # 是否需要初始化数据库
    # write_mode = models.BooleanField(default=False)   # 该环境是否只能执行读相关用例
    name = models.CharField(max_length=50)
    gsdm = models.CharField(max_length=15, default='0')  # 公司代码
    base_url = models.URLField(max_length=200)
    base_headers = models.TextField(max_length=1000, default='', blank=True)
    dataBase_host = models.CharField(max_length=15, null=True, blank=True)
    dataBase_port = models.CharField(max_length=5, null=True, blank=True)
    dataBase_name = models.CharField(max_length=50, null=True, blank=True)
    dataBase_user = models.CharField(max_length=50, null=True, blank=True)
    dataBase_pwd = models.CharField(max_length=20, null=True, blank=True)
    dataBase_type = models.CharField(max_length=10,
                                     choices=(('mysql', 'mysql'),
                                              ('sqlServer', 'sqlServer'),
                                              ('oracle', 'oracle')
                                              ),
                                     default='sqlServer')

    def __str__(self):
        return self.name


class EnvParam(models.Model):
    status = models.BooleanField(default=True)
    range = models.CharField(max_length=4,
                             choices=(('env', 'env'),),
                             default='env')
    type = models.CharField(max_length=4, choices=(('str', 'str'),
                                                   ('sql', 'sql'),
                                                   ('time', 'time')),
                            default='string')
    name = models.CharField(max_length=20, unique=True)
    value = models.CharField(max_length=200)
    mark = models.CharField(max_length=50, null=True, blank=True)
    real_value = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


# 用例组
class Group(models.Model):
    status = models.BooleanField(default=True)
    is_init = models.BooleanField(default=False)    # 是否初始化用例组
    name = models.CharField(max_length=50, unique=True)
    preVar = models.TextField(max_length=1000, default='', blank=True)
    remark = models.TextField(blank=True, null=True)
    result = models.BooleanField(default=True)
    msg = models.TextField(max_length=1000, default='', blank=True)
    # size = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Case(models.Model):
    status = models.BooleanField(default=True)
    type = models.CharField(max_length=10, default='read',
                            choices=(('write', 'write'),
                                     ('read', 'read')),
                            )
    name = models.CharField(max_length=50, unique=True)
    preVar = models.TextField(max_length=1000, default='', blank=True)
    result = models.BooleanField(default=True)
    msg = models.TextField(max_length=1000, default='', blank=True)
    # size = models.IntegerField(default=0)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GroupCase(models.Model):
    status = models.BooleanField(default=True)  # 状态
    group = models.ForeignKey(Group, null=True)
    case = models.ForeignKey(Case, null=True)

    class Meta:
        unique_together = ('case', 'group')

    def __int__(self):
        return self.id


class Step(models.Model):
    status = models.BooleanField(default=True)
    pre_var = models.TextField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    request_type = models.CharField(max_length=4, choices=(('get', 'get'), ('post', 'post')), default='get')
    request_url = models.CharField(max_length=200, null=True, blank=True)
    request_headers = models.TextField(max_length=1000, null=True, blank=True)
    request_query = models.TextField(max_length=1024, null=True, blank=True)
    request_body = models.TextField(max_length=2048, null=True, blank=True)
    response_source = models.CharField(max_length=50,
                                       choices=(('text', 'text'),
                                                ('headers["Set-Cookie"]', 'headers["Set-Cookie"]')),
                                       default='text')
    response_type = models.CharField(max_length=20,
                                     choices=(('string', 'string'), ('json', 'json'), ('html', 'html')),
                                     default='html')
    post_var = models.TextField(max_length=1000, null=True, blank=True)
    assert_var = models.TextField(max_length=1000, null=True, blank=True)
    repeat = models.IntegerField(default=1)
    remark = models.TextField(blank=True, null=True)
    result = models.BooleanField(default=True)
    msg = models.TextField(max_length=1000, default='', blank=True)

    def __str__(self):
        return self.name


class CaseStep(models.Model):
    status = models.BooleanField(default=True)  # 状态
    case = models.ForeignKey(Case, null=True)
    step = models.ForeignKey(Step, null=True)

    # class Meta:
    #     unique_together = ('case', 'step')

    def __int__(self):
        return self.id


# # 步骤请求
# class RequestInfo(models.Model):
#     status = models.BooleanField(default=True)
#     name = models.CharField(max_length=50)  # 请求名称
#     type = models.CharField(max_length=4, choices=(('get', 'get'), ('post', 'post')), default='get')
#     url = models.CharField(max_length=200, null=True, blank=True)
#     headers = models.TextField(max_length=1000, null=True, blank=True)
#     query = models.TextField(max_length=1000, null=True, blank=True)
#     body = models.TextField(max_length=1000, null=True, blank=True)

    # def __str__(self):
    #     return self.name


# class StepPostProcessor(models.Model):
#     status = models.BooleanField(default=True)  # 状态
#     step = models.ForeignKey(Step, null=True)
#     postProcessor = models.ForeignKey(PostProcessor, null=True)
#
#     def __int__(self):
#         return self.id

# class PostProcessor(models.Model):
#     name = models.CharField(max_length=50)
#     status = models.BooleanField(default=True)
#     source = models.CharField(max_length=50,
#                               choices=(('text', 'text'),
#                                        ('headers["Set-Cookie"]', 'headers["Set-Cookie"]')),
#                               default='Text')
#     type = models.CharField(max_length=20, choices=(('string', 'string'), ('json', 'json'), ('html', 'html')),
#                             default='html')
#     postVar = models.TextField(max_length=1000, null=True, blank=True)
#     assertVar = models.TextField(max_length=1000, null=True, blank=True)
#
#     def __str__(self):
#         return self.name

# # 前置变量组
# class PreVarGroup(models.Model):
#     status = models.BooleanField(default=True)
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name

# class GroupParam(models.Model):
#     status = models.BooleanField(default=True)
#     range = models.CharField(max_length=4,
#                              choices=(('group', 'group'),),
#                              default='group')
#     type = models.CharField(max_length=4, choices=(('str', 'str'),
#                                                    ('sql', 'sql'),
#                                                    ('time', 'time')),
#                             default='string')
#     name = models.CharField(max_length=20, unique=True)
#     value = models.CharField(max_length=50)
#     mark = models.CharField(max_length=50, null=True, blank=True)
#     real_value = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return self.name


# class CaseParam(models.Model):
#     status = models.BooleanField(default=True)
#     range = models.CharField(max_length=4,
#                              choices=(('case', 'case'),),
#                              default='case')
#     type = models.CharField(max_length=4, choices=(('str', 'str'),
#                                                    ('sql', 'sql'),
#                                                    ('time', 'time')),
#                             default='string')
#     name = models.CharField(max_length=20, unique=True)
#     value = models.CharField(max_length=50)
#     mark = models.CharField(max_length=50, null=True, blank=True)
#     real_value = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return self.name

# 修改创建时间类型
# ALTER TABLE  `sign_event` CHANGE  `create_time`  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# ALTER TABLE  `sign_guest` CHANGE  `create_time`  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
