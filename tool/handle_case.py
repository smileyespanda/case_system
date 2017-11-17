# coding:utf-8
from urllib.parse import urlencode
# from tool import handle_log
import requests
from django.shortcuts import get_object_or_404
from sign.models import *
from tool.handle_string import StringHandler
from tool.handle_time import TimeHandler


class CaseHandler(object):
    def __init__(self, case_id):
        try:
            self.base_url = ''
            self.base_headers = {}
            self.request_handler = requests.session()
            self.write_mode = False
            self.dict_var = {}
            self.init_config()
            self.set_env()
            self.reset_env()
            self.run_init_case()
            self.case_id = case_id
            self.step_msg = ''
        except Exception:
            print('<error> 初始化失败，用例均未执行！！！\n')
            raise False

    def init_config(self):
        try:
            try:
                config = get_object_or_404(Config, status=True)
                print('<info> ~~~~~~~~~本次使用的环境配置是：%s~~~~~~~~~~\n' % config.name)
            except Exception:
                print('<error> 没有有效的环境配置，请确保一套环境配置是有效状态\n')
                raise False
            self.write_mode = config.write_mode
            if self.write_mode:
                print('<warning> 本次环境禁止执行《写》用例！！！\n')
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

    def set_env(self):
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

    def reset_env(self):
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

    def run_init_case(self):
        # 先执行初始化用例
        try:
            init_group = get_object_or_404(Group, is_init=True)
            init_group.result = True
            init_group.msg = ''
        except Exception:
            print('<warning> 没有设置初始用例组，请确认。')
            raise False
        # Group.objects.filter(name=u'初始用例组')
        list_init_case = Case.objects.filter(is_init=True)
        for init_case in list_init_case:
            self.case_id = init_case.id
            try:
                print('<info> 开始执行初始化用例~')
                assert self.run_case(False)
            except Exception:
                init_group.result = False
                init_group.msg = init_case.name
                print('<error> 执行初始用例失败：%s\n' % init_case.name)
                raise False
            finally:
                init_group.save()

    def run_case(self, non_init=True):
        # 判断case是否存在，通过id查找，不存在404
        case = get_object_or_404(Case, id=self.case_id, status=True)
        case.msg = ''
        case.result = True
        if non_init:
            if case.is_init:
                return True
        print(u"<info> **************开始执行用例********************\n")
        print(u"<info> id：%d; name：%s\n" % (case.id, case.name))
        try:
            if case.type == 'write' and not self.write_mode:
                print('<warning> 该环境禁止执行《读》用例\n')
                return True
            self.reset_var(case.preVar)
            case_step_list = CaseStep.objects.filter(case_id=self.case_id, status=True)
            step_list = []
            for case_step in case_step_list:
                step_id = case_step.step_id
                step = get_object_or_404(Step, id=step_id, status=True)
                step_list.append(step)
            if len(step_list) < 1:
                print('<warning> 该用例没有步骤可执行')
                case.msg = '该用例没有步骤可执行'
                case.save()
                return True
            for step in step_list:
                if not self.run_step(step):
                    raise False
        except Exception:
            case.result = False
            print(u"<error> **************用例执行失败************************* \n")
            return False
        finally:
            # 保存case更新
            case.save()
        print(u"<info> ***********用例执行成功************************* \n")
        return True

    def send_request(self, step):
        print(u"<info> 开始发送请求 \n")
        send_url = self.base_url
        headers = self.base_headers
        send_url += step.request_url
        send_type = step.request_type
        print(u"<info> 开始替换request参数中的变量 \n")
        try:
            try:
                request_headers = self.replace_var(step.request_headers)
                request_query = self.replace_var(step.request_query)
                request_body = self.replace_var(step.request_body)
            except None:
                print('<error> 替换request参数中的变量失败')
                raise False
            print(u"<info> 开始将request的字典类型参数转化为字典\n")
            try:
                dict_headers = StringHandler.string_to_dict(request_headers)
                dict_query = StringHandler.string_to_dict(request_query)
                dict_body = StringHandler.string_to_dict(request_body)
            except Exception:
                print('<error> request的字典类型参数格式错误')
                self.step_msg = 'request的字典类型参数格式错误'
                raise False
            headers = dict(headers, **dict_headers)
            dict_query = StringHandler.encode_dict(dict_query)
            query_string = urlencode(dict_query)
            send_url += query_string
            print('<info> 请求的url: {}\n'.format(send_url))
            data = urlencode(dict_body)
            if send_type.lower() == 'post':
                response = self.request_handler.post(send_url, data=data, headers=headers)
            else:
                response = self.request_handler.get(send_url, data=data, headers=headers)
            if response.status_code != 200:
                print(u'<error> 请求状态异常：%d\n' % response.status_code)
                self.step_msg += u'<error> 请求状态异常：%d\n' % response.status_code
                raise False
        except Exception:
            print(u"<error> 请求发送失败: \n"
                  u"        request_type：{1} \n"
                  u"        request_url:{2}\n"
                  u"        request_headers: {3}"
                  u"        request_query: {4}\n"
                  u"        request_body: {5}\n".format(send_type, send_url, step.request_headers,
                                                        step.request_query, step.request_body))
            raise False
        print(u"<info> 请求发送成功！ \n")
        return response

    def run_step(self, step):
        print(u"<info> -----------开始执行步骤------------------\n")
        print(u"<info> id：%d; name：%s\n" % (step.id, step.name))
        step.result = True
        self.step_msg = ''
        try:
            response = self.send_request(step)
            self.exe_post_processor(response, step)
        except Exception:
            step.result = False
            print(u"<error> -----------步骤执行失败------------------\n")
            return False
        finally:
            step.msg = self.step_msg
            step.save()
        print(u"<info> -----------步骤执行成功！-----------------！\n")
        return True

    def exe_post_processor(self, response, step):
        try:
            source_expression = 'response.' + step.response_source
            str_source_type = step.response_type
            print(u'<info> 开始预处理PostVar\n')
            print(u'<info> 获取接口返回的信息：信息源: %s；信息类型: %s\n' % (step.response_source, str_source_type))
            str_source_text = eval(source_expression)
            if not str_source_text:
                print(u'<warning> 信息源为空')
            str_post_var = step.post_var
            if not str_post_var:
                return True
            try:
                dict_post_var = StringHandler.string_to_dict(self.replace_var(str_post_var))
            except Exception:
                print(u'<error> PostVar格式错误请检查: %s\n' % str_post_var)
                self.step_msg = u'<error> PostVar格式错误请检查: %s\n' % str_post_var
                raise False
            for var_name, var_expression in dict_post_var.items():
                print(u'<info> 设置变量：%s；表达式: %s\n' % (var_name, var_expression))
                try:
                    var_value = StringHandler.get_string_attr(str_source_text, str_source_type, var_expression)
                    self.dict_var[var_name] = var_value
                    print(u'<info> 设置成功；变量值：%s\n' % var_value)
                    if var_value is None:
                        print(u'<warning> 设置可能有误！\n')
                except Exception:
                    print(u'<error> 设置失败！\n')
                    self.step_msg += u'设置PostVar失败，变量名: %s\n' % var_name
                    raise False
            print(u'<info> PostVar处理成功！\n')
            self.assert_var(step.assert_var)
        except Exception:
            raise False

    def assert_var(self, str_assert_var):
        if not str_assert_var:
            print(u'<warning> 没有设置数据校验\n')
            return True
        print(u'<info> 开始校验数据AssertVar\n')
        print(u'<info> 开始替换AssertVar中的变量\n')
        str_assert_var = self.replace_var(str_assert_var)
        try:
            dict_assert_var = StringHandler.string_to_dict(str_assert_var)
        except Exception:
            print(u'<error> AssertVar数据格式错误, %s\n' % str_assert_var)
            self.step_msg += u'AssertVar数据格式错误, %s\n' % str_assert_var
            raise False
        for k, v in dict_assert_var.items():
            v = v.replace("\r", '').replace("\n", '')
            v_mid = StringHandler.get_middle_str(v, "\"", "\".")
            v_mid_new = v_mid.replace("\"", "").replace("\'", "")
            v = v.replace(v_mid, v_mid_new)
            print(u'<info> 校验变量：%s, 表达式：%s\n' % (k, v))
            try:
                real_result = eval(v)
            except Exception:
                print(u'<error> 表达式格式错误！\n')
                raise False
            final_result = real_result
            if k.startswith("!"):
                final_result = not final_result
            try:
                assert final_result
            except AssertionError:
                print(u'<error> 数据校验失败！\n')
                self.step_msg += u'数据校验失败\n k: %s; v: %s\n' % (k, v)
                raise False
        print(u'<info> AssertVar数据校验成功！\n')

    def replace_var(self, str_var):
        list_params = StringHandler.get_middle_str_list(str_var, '$', '$')
        for param in list_params:
            param_key = '$'+param+'$'
            if param not in self.dict_var:
                print(u'<error> 没有预先设置变量：%s\n' % param_key)
                self.step_msg += u'没有预先设置变量：%s\n' % param_key
                raise None
            param_value = self.dict_var.get(param)
            if param_value is None:
                param_value = ''
            str_var = str_var.replace(param_key, param_value)
        return str_var

    def reset_var(self, str_var_param):
        print(u"<info> 开始为用例设置全局变量 \n")
        print(u'<info> 替换PostVar中的变量\n')
        str_var_param = self.replace_var(str_var_param)
        try:
            dict_var_param = StringHandler.string_to_dict(str_var_param)
            for k, v in dict_var_param.items():
                print(u"<info> k: %s, v: %s\n" % (k, v))
                self.dict_var[k] = v
        except Exception:
            print(u'<error> 设置前置变量出错: %s\n' % str_var_param)
            raise False
        print(u"<info> 用例设置全局变量设置成功！ \n")
