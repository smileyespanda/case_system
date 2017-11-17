# coding:utf-8
from django.shortcuts import get_object_or_404
from sign.models import *
from tool.handle_time import TimeHandler


class PublicHandler(object):
    dict_var = {}
    has_init_config = False
    has_init_group = False
    has_set_env = False
    has_reset_env = False
    has_init_db = False
    base_url = ''
    write_mode = False
    base_headers = {}

    def init_config(self):
        if self.has_init_config:
            return True
        try:
            try:
                config = get_object_or_404(Config, status=True)
                print('<info> ~~~~~~~~~本次使用的环境配置是：%s~~~~~~~~~~\n' % config.name)
            except Exception:
                print('<error> 没有有效的环境配置，请确保一套环境配置是有效状态\n')
                raise None
            self.write_mode = config.write_mode
            if self.write_mode:
                print('<warning> 本次环境开启了write_mode！！！\n')
            self.base_url = config.base_url
            print('<warning> 本次环境的基础url: %s\n' % self.base_url)
            try:
                self.base_headers = eval(config.base_headers)
            except Exception:
                print('<error> Base Headers数据格式错误！\n')
                raise False
        except Exception:
            print('<error> 初始化环境配置失败！\n')
            raise False
        self.has_init_config = True

    def set_env(self):
        if self.has_set_env:
            return True
        print('<info> 开始初始化环境变量\n')
        list_env_param = EnvParam.objects.filter(status=True)
        for env_param in list_env_param:
            env_type = env_param.type
            if env_type == 'sql':
                continue
            env_name = env_param.name
            env_value = env_param.value
            # print('<info> 变量信息--类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
            try:
                if env_type == 'time':
                    list_param = env_value.split(",")
                    env_value = TimeHandler.getStrTime(list_param[0], int(list_param[1]), int(list_param[2]))
                env_param.real_value = env_value
                env_param.save()
                self.dict_var[env_name] = env_value
            except Exception:
                print('<error> 设置该环境变量失败:\n'
                      '        类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
                raise False
        print('<info> 初始化环境变量成功~\n')
        self.has_set_env = True

    def reset_env(self):
        if self.has_reset_env:
            return True
        print('<info> 开始重置环境变量\n')
        list_env_param = EnvParam.objects.filter(status=True, type='sql')
        for env_param in list_env_param:
            env_type = env_param.type
            env_name = env_param.name
            env_value = self.replace_var(env_param.value)
            try:
                env_param.real_value = env_value
                env_param.save()
                self.dict_var[env_name] = env_value
            except Exception:
                print('<error> 重置环境变量失败:\n'
                      '        类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
                raise False
        print('<info> 重置环境变量成功~\n')
        self.has_reset_env = True

