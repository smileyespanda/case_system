# coding:utf-8
from urllib.parse import urlencode

import requests

from sign.models import *
from tool import create_case
from tool import handle_log
from tool.handle_db import DBHandler
from tool.handle_string import StringHandler
from tool.handle_time import TimeHandler
import os


class GroupCaseHandler(object):
    request_handler = requests.session()
    dict_var = {}
    msg = ""
    need_init_db = False
    db_handler = None
    group = None
    case = None
    step = None
    group_msg = ''
    case_msg = ''
    step_msg = ''
    group_result = False
    case_result = False
    step_result = False
    base_url = ''
    base_headers = {}
    write_mode = False
    has_init = False

    @classmethod
    def __init__(cls):
        cls.has_init = False

    @classmethod
    def print_log(cls):
        handle_log.output_log()
        print(cls.msg)

    @classmethod
    def init_db(cls):
        # 初始化数据库
        if cls.need_init_db:
            handle_log.build_log("<info> 开始初始化数据库\n")
            try:
                cls.db_handler = DBHandler()
                cls.db_handler.connect_db()
                # 读取初始化数据库的sql
                init_db_file = open("init_db.sql", "rb")
                init_sql = init_db_file.read().decode("utf8")
                init_db_file.close()
                # 替换初始化sql中的变量
                init_sql = cls.replace_var(init_sql, "INIT_SQL")
                # 执行初始化数据的sql
                cls.db_handler.exec_non_query(init_sql)
            except Exception as e:
                handle_log.build_log("<error> 初始化数据库失败\n")
                print(e)
                raise e

    @classmethod
    def init_config(cls):
        try:
            try:
                config_list = Config.objects.filter(status=True)
                if len(config_list) != 1:
                    raise ValueError
                config = config_list[0]
                handle_log.build_log('<info> ~~~~~~~~~本次使用的环境配置是：%s~~~~~~~~~~\n' % config.name)
            except Exception as e:
                handle_log.build_log('<error> 环境配置问题，没有启用任何环境或者启用的环境不止一个\n')
                cls.group_msg = '没有启用任何环境或者启用的环境不止一个'
                raise e
            cls.dict_var["gsdm"] = config.gsdm
            cls.write_mode = config.init_db
            cls.need_init_db = config.init_db
            if cls.write_mode:
                handle_log.build_log('<warning> 本次环境开启了write_mode！！！\n')
            cls.base_url = config.base_url
            handle_log.build_log('<info> 本次环境的基础url: %s\n' % cls.base_url)
            try:
                cls.base_headers = eval(config.base_headers)
            except Exception as e:
                handle_log.build_log('<error> Base Headers数据格式错误！\n')
                cls.group_msg = '环境配置BaseHeaders格式错误'
                raise e
        except Exception as e:
            handle_log.build_log('<error> 初始化环境配置失败！\n{}\n'.format(e))
            cls.case_msg = '初始化环境配置失败,用例未执行'
            cls.update_group_case()
            raise e

    @classmethod
    def set_env(cls):
        handle_log.build_log('<info> 开始初始化环境变量\n')
        list_env_param = EnvParam.objects.filter(status=True)
        for env_param in list_env_param:
            env_type = env_param.type
            if env_type == 'sql':
                continue
            env_name = env_param.name
            env_value = env_param.value
            # handle_log.build_log('<info> 变量信息--类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
            try:
                if env_type == 'time':
                    list_param = env_value.split(",")
                    env_value = TimeHandler.getStrTime(list_param[0], int(list_param[1]), int(list_param[2]))
                env_param.real_value = env_value
                env_param.save()
                cls.dict_var[env_name.lower()] = env_value
            except Exception as e:
                cls.case_msg = '环境初始化失败，用例未执行'
                cls.group_msg = '环境变量有误：%s' % env_name
                handle_log.build_log('<error> 设置该环境变量失败:\n'
                                     '        类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
                raise e
        handle_log.build_log('<info> 初始化环境变量成功~\n')

    @classmethod
    def reset_env(cls):
        # 如果初始化db的开关没开就不去更新sql变量的值
        if not cls.need_init_db:
            return True
        handle_log.build_log('<info> 开始重置环境变量\n')
        list_env_param = EnvParam.objects.filter(status=True, type='sql')
        for env_param in list_env_param:
            env_type = env_param.type
            env_name = env_param.name
            origin_value = env_param.value
            origin_value = cls.replace_var(origin_value, "EnvParams_sql")
            # print("sql", origin_value)
            env_value = cls.db_handler.exec_query(origin_value)[0][0]
            try:
                env_param.real_value = env_value
                env_param.save()
                cls.dict_var[env_name.lower()] = str(env_value)
            except Exception as e:
                cls.db_handler.close_db()
                cls.case_msg = '环境初始化失败，用例未执行'
                cls.group_msg = '环境变量有误：%s' % env_name
                handle_log.build_log('<error> 重置环境变量失败:\n'
                                     '        类型: %s; 名称：%s; 表达式：%s\n' % (env_type, env_name, env_value))
                raise e
        handle_log.build_log('<info> 重置环境变量成功~\n')
        cls.db_handler.close_db()

    @classmethod
    def set_group_var(cls):
        handle_log.build_log('<info> 开始设置group的PreVar\n')
        try:
            group_pre_var = cls.group.preVar
            group_pre_var = cls.replace_var(group_pre_var, "Group.PreVar")
            dict_group_pre_var = StringHandler.string_to_dict(group_pre_var)
            for k, v in dict_group_pre_var.items():
                cls.dict_var[k.lower()] = v
        except Exception as e:
            cls.case_msg = 'Group.preVar设置出错，用例未执行'
            cls.group_msg = 'Group设置PreVar失败'
            raise e

    @classmethod
    def run_case(cls, group_id, case_id):
        # 判断case是否存在，通过id查找，不存在404
        cls.group_msg = ""
        cls.case_msg = ""
        cls.step = None
        try:
            cls.group = Group.objects.get(id=group_id)
            cls.case = Case.objects.get(id=case_id)
            try:
                if cls.group.is_init and not cls.has_init:
                    # 如果是初始化用例组则需要进行环境初始化
                    cls.init_config()
                    cls.set_env()
                    cls.init_db()
                    cls.reset_env()
                    # 初始化成功之后将初始化开关关闭以免重复初始化
                    cls.has_init = True
            except Exception as e:
                cls.case_result = False
                cls.case_msg = "环境初始化失败"
                raise e
            cls.set_group_var()
            cls.case_msg = ''
            handle_log.build_log(u"<info> **************开始执行用例********************\n")
            handle_log.build_log(u"<info> group_id：%d; group_name：%s\n" % (cls.group.id, cls.group.name))
            handle_log.build_log(u"<info> case_id：%d; case_name：%s\n" % (cls.case.id, cls.case.name))
            # 如果用例组或者用例无效，则不往下执行
            if not (cls.group and cls.case):
                handle_log.build_log(u"<warning> 当前用例组或者用例无效，不予执行")
                return True
            # 如果环境配置中write_mode是关闭的,则不执行读用例
            if cls.case.type == 'write' and not cls.write_mode:
                handle_log.build_log('<warning> 该环境禁止执行《读》用例\n')
                cls.case_msg = u'该环境禁止《写》用例'
                return True
            try:
                # 将用例中的前置变量存储到内存中
                cls.reset_var(cls.case.preVar)
                # 查找用例挂载的步骤
                assert cls.run_case_step()
            except Exception as e:
                # cls.group_msg = cls.case.name
                handle_log.build_log(u"<error> **************用例执行失败************************* \n")
                raise e
            handle_log.build_log(u"<info> ***********用例执行成功************************* \n")
            cls.case_result = True
            cls.group_result = True
            return True
        except Exception:
            cls.case_result = False
            cls.group_result = False
            return False
        finally:
            cls.print_log()
            cls.update_group_case()

    @classmethod
    def run_case_step(cls):
        case_step_list = CaseStep.objects.filter(case_id=cls.case.id, status=True)
        for case_step in case_step_list:
            list_step = Step.objects.filter(id=case_step.step_id, status=True)
            # 初始化步骤
            for step in list_step:
                step.msg = ''
                step.result = True
                step.save()
        for case_step in case_step_list:
            step_id = case_step.step_id
            cls.step = Step.objects.get(id=step_id, status=True)
            if not cls.step:
                return True
            try:
                repeat_num = cls.step.repeat
                for i in range(repeat_num):
                    assert cls.run_step()
            except AssertionError:
                # cls.case_msg = cls.step.name
                return False
        return True

    @classmethod
    def send_request(cls):
        handle_log.build_log(u"<info> 开始发送请求 \n")
        send_url = cls.base_url
        headers = cls.base_headers
        send_url += cls.replace_var(cls.step.request_url, "Step.RequestUrl")
        send_type = cls.step.request_type
        handle_log.build_log(u"<info> 开始替换request参数中的变量 \n")
        try:
            request_headers = cls.replace_var(cls.step.request_headers, "Step.RequestHeaders")
            request_query = cls.replace_var(cls.step.request_query, "Step.RequestQuery")
            request_body = cls.replace_var(cls.step.request_body, "Step.RequestBody")
            dict_headers = StringHandler.string_to_dict(request_headers)
            dict_query = StringHandler.string_to_dict(request_query)
            dict_body = StringHandler.string_to_dict(request_body)
            headers = dict(headers, **dict_headers)
            dict_query = StringHandler.encode_dict(dict_query)
            query_string = urlencode(dict_query)
            send_url += query_string
            handle_log.build_log('<info> 请求的url: {}\n'.format(send_url))
            dict_body = StringHandler.encode_dict(dict_body)
            data = urlencode(dict_body)
            if send_type.lower() == 'post':
                response = cls.request_handler.post(send_url, data=data, headers=headers)
            else:
                response = cls.request_handler.get(send_url, data=data, headers=headers)
            if response.status_code != 200:
                handle_log.build_log(u'<error> 请求状态异常：%d\n' % response.status_code)
                cls.step_msg = u'请求状态异常：%d' % response.status_code
                raise ValueError
        except Exception as e:
            handle_log.build_log(u"<error> 请求发送失败: \n"
                                 u"        request_type：{1} \n"
                                 u"        request_url:{2}\n"
                                 u"        request_headers: {3}"
                                 u"        request_query: {4}\n"
                                 u"        request_body: {5}\n".format(send_type, send_url,
                                                                       cls.step.request_headers,
                                                                       cls.step.request_query, cls.step.request_body))
            raise e
        handle_log.build_log(u"<info> 请求发送成功！ \n")
        return response

    @classmethod
    def run_step(cls):
        cls.step_msg = ''
        cls.step_result = True
        handle_log.build_log(u"<info> -----------开始执行步骤------------------\n")
        handle_log.build_log(u"<info> id：%d; name：%s\n" % (cls.step.id, cls.step.name))
        try:
            response = cls.send_request()
            try:
                if cls.step.name == '初始化菜单':
                    str_info = response.text
                    create_case.update_group_info(str_info)
            except Exception as e:
                cls.step_result = False
                cls.step_msg = '初始化用例组信息失败'
                handle_log.build_log(u"<error> -----------初始化用例组信息失败------------------\n")
                raise e
            cls.exe_post_processor(response)
            handle_log.build_log(u"<info> -----------步骤执行成功！-----------------！\n")
        except Exception:
            cls.step_result = False
            handle_log.build_log(u"<error> -----------步骤执行失败------------------\n")
            return False
        finally:
            cls.update_step()
        return True

    @classmethod
    def exe_post_processor(cls, response):
        try:
            source_expression = 'response.' + cls.step.response_source
            str_source_type = cls.step.response_type
            handle_log.build_log(u'<info> 开始预处理PostVar\n')
            handle_log.build_log(u'<info> 获取接口返回的信息：信息源: %s；信息类型: %s\n' %
                                 (cls.step.response_source, str_source_type))
            str_source_text = eval(source_expression)
            str_source_text = str_source_text.replace("'", "\"")
            if not str_source_text:
                handle_log.build_log(u'<warning> 信息源为空')
            str_post_var = cls.step.post_var
            if not str_post_var:
                return True
            dict_post_var = StringHandler.string_to_dict(cls.replace_var(str_post_var, "Step.PostVar"))
            for var_name, var_expression in dict_post_var.items():
                handle_log.build_log(u'<info> 设置变量：%s；表达式: %s\n' % (var_name, var_expression))
                try:
                    var_value = StringHandler.get_string_attr(str_source_text, str_source_type, var_expression)
                    cls.dict_var[var_name.lower()] = var_value
                    handle_log.build_log(u'<info> 设置成功；变量值：%s\n' % var_value)
                    if var_value is None:
                        handle_log.build_log(u'<warning> 设置可能有误！\n')
                except Exception as e:
                    handle_log.build_log(u'<error> 设置失败！\n')
                    cls.step_msg = u'设置PostVar失败: %s\n' % var_name
                    raise e
            handle_log.build_log(u'<info> PostVar处理成功！\n')
            cls.assert_var(cls.step.assert_var)
        except Exception as e:
            cls.step_result = False
            raise e

    @classmethod
    def assert_var(cls, str_assert_var):
        if not str_assert_var:
            handle_log.build_log(u'<warning> 没有设置数据校验\n')
            return True
        handle_log.build_log(u'<info> 开始校验数据AssertVar\n')
        handle_log.build_log(u'<info> 开始替换AssertVar中的变量\n')
        str_assert_var = cls.replace_var(str_assert_var, "Step.AssertVar")
        try:
            dict_assert_var = StringHandler.string_to_dict(str_assert_var)
        except Exception as e:
            handle_log.build_log(u'<error> AssertVar数据格式错误, %s\n' % str_assert_var)
            cls.step_msg = u'AssertVar数据格式错误\n'
            raise e
        for k, v in dict_assert_var.items():
            v = v.replace("\r", '').replace("\n", '')
            # v_mid = StringHandler.get_middle_str(v, "\"", "\".")
            # v_mid_new = v_mid.replace("\"", "").replace("\'", "")
            # v = v.replace(v_mid, v_mid_new)
            handle_log.build_log(u'<info> 校验变量：%s, 表达式：%s\n' % (k, v))
            try:
                real_result = eval(v)
            except Exception as e:
                handle_log.build_log(u'<error> 表达式格式错误！\n')
                cls.step_msg = u'AssertVar表达式错误-k: %s; v: %s\n' % (k, v)
                raise e
            final_result = real_result
            if k.startswith("!"):
                final_result = not final_result
            try:
                assert final_result
            except AssertionError:
                handle_log.build_log(u'<error> 数据校验失败！\n')
                cls.step_msg = u'AssertVar校验失败\n k: %s; v: %s\n' % (k, v)
                raise AssertionError
        handle_log.build_log(u'<info> AssertVar数据校验成功！\n')

    @classmethod
    def replace_var(cls, str_var, str_type):
        try:
            if str_type != "EnvParams_sql":
                handle_log.build_log(u"<info> 开始替换%s中的变量 \n" % str_type)
            list_params = StringHandler.get_middle_str_list(str_var, '$', '$')
            for param in list_params:
                param_new = param.lower()
                param_key = '$'+param+'$'
                # handle_log.build_log(u"<info> 替换变量k: %s\n" % param_key)
                if param_new not in cls.dict_var:
                    handle_log.build_log(u'<error> 替换变量失败，没有前置变量：%s\n' % param_key)
                    error_msg = "%s中没有预先设置变量：%s\n" % (str_type, param_key)
                    if cls.step:
                        cls.step_msg = error_msg
                    raise (ValueError, error_msg)
                param_value = cls.dict_var.get(param_new)
                if param_value is None:
                    param_value = ''
                # handle_log.build_log(u"<info> 替换成功k~v: %s~%s\n" % (param_key,param_value))
                str_var = str_var.replace(param_key, param_value)   # .replace("\"","").replace("'","")
            return str_var
        except Exception as e:
            # print(str_var)
            handle_log.build_log('<error> 替换%s参数中的变量失败' % str_type)
            handle_log.build_log('<error> %s' % e)
            raise e

    @classmethod
    def reset_var(cls, str_var_param):
        handle_log.build_log(u"<info> 开始设置PostVar \n")
        handle_log.build_log(u'<info> 开始替换PostVar中的变量\n')
        str_var_param = cls.replace_var(str_var_param, "EnvParams")
        try:
            dict_var_param = StringHandler.string_to_dict(str_var_param)
            for k, v in dict_var_param.items():
                handle_log.build_log(u"<info> k: %s, v: %s\n" % (k, v))
                cls.dict_var[k.lower()] = v
        except Exception as e:
            handle_log.build_log(u'<error> 设置前置变量出错: %s\n' % str_var_param)
            cls.case_msg = u'设置前置变量出错: %s\n' % str_var_param
            raise e
        handle_log.build_log(u"<info> 用例设置全局变量设置成功！ \n")

    @classmethod
    def update_group_case(cls):
        if cls.case:
            cls.case.result = cls.case_result
            cls.case.msg = cls.case_msg
            cls.case.save()
        if cls.group:
            if cls.group.result:
                cls.group.result = cls.group_result
            cls.group.msg = cls.group_msg
            cls.group.save()

    @classmethod
    def update_step(cls):
        if cls.step:
            cls.step.result = cls.step_result
            cls.step.msg = cls.step_msg
            cls.step.save()



