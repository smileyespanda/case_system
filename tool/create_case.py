# coding:utf-8
from tool.handle_string import StringHandler
from sign.models import *
from django.shortcuts import get_object_or_404
import json
import yaml
import re


def copy_group(source_group_name, target_group_name):
    try:
        source_group = get_object_or_404(Group, name=source_group_name)
    except Exception:
        msg = '<warning> 源组不存在, 请输入已存在的用例组名称： {}\n'.format(source_group_name)
        print(msg)
        return msg, False
    dec_name_list = target_group_name.split("-")
    size = len(dec_name_list)
    if size > 3 or size < 2:
        msg = '<warning> 目标组名称不合法，请重新输入： {}\n'.format(target_group_name)
        return msg, False
    souce_group_case_list = GroupCase.objects.filter(group_id=source_group.id, status=True)
    source_case_id_list = []
    for source_group_case in souce_group_case_list:
        source_case_id_list.append(source_group_case.case_id)
    try:
        get_object_or_404(Group, name=target_group_name)
        msg = '<warning> 目标用例组已存在，不能创建相同名称的用例组：{}！\n'.format(target_group_name)
        return msg, False
    except Exception:
        msg = '<info> 创建新的用例组：%s\n' % target_group_name
        Group.objects.create(name=target_group_name,
                             is_init=source_group.is_init,
                             preVar=source_group.preVar,
                             remark="copy %s" % source_group_name)
        target_group = get_object_or_404(Group, name=target_group_name)
        for source_case_id in source_case_id_list:
            msg = ""
            source_case = get_object_or_404(Case, id=source_case_id)
            source_case_name = source_case.name
            target_case_name = source_case_name+".copy_" + str(target_group.id)
            try:
                result = copy_case(source_case_name, target_case_name)
                target_case_id = get_object_or_404(Case, name=target_case_name).id
                # 关联复制的用例组和用例
                GroupCase.objects.create(case_id=target_case_id, group_id=target_group.id)
                msg += result[0]
                assert result[1]
            except Exception:
                msg += "<error> 复制用例失败， 用例名称:{}\n".format(target_case_name)
                return msg, False
        msg += "<info> 成功复制用例组：《%s》>>《%s》\n" % (source_group_name, target_group_name)
        print(msg)
        return msg, True


def copy_case(source_case_name, target_case_name):
    try:
        source_case = get_object_or_404(Case, name=source_case_name)
    except Exception:
        msg = '<warning> 复制源不存在, 请输入已存在的用例名称： {}\n'.format(source_case_name)
        print(msg)
        return msg, False
    souce_case_step_list = CaseStep.objects.filter(case_id=source_case.id, status=True)
    source_step_id_list = []
    for source_case_step in souce_case_step_list:
        source_step_id_list.append(source_case_step.step_id)
    try:
        get_object_or_404(Case, name=target_case_name, type=source_case.type,preVar=source_case.preVar,
                          remark="复制于%s"%source_case_name)
        msg = '<warning> 不能创建相同名称的用例，目标用例名已存在：{}！\n'.format(target_case_name)
        return msg, False
    except Exception:
        msg = '<info> 创建新用例：%s\n' % target_case_name
        Case.objects.create(name=target_case_name)
        target_case_id = Case.objects.get(name=target_case_name).id
        # 将步骤id排序，因为执行的步骤和id顺序有关
        source_step_id_list.sort()
        for source_step_id in source_step_id_list:
            # 获取复制源步骤信息
            source_step = get_object_or_404(Step, id=source_step_id)
            # 复制一个步骤
            copy_step_name = source_step.name+".copy_" + str(target_case_id)
            Step.objects.create(pre_var=source_step.pre_var,
                                name=copy_step_name,
                                request_type=source_step.request_type,
                                request_url=source_step.request_url,
                                request_headers=source_step.request_headers,
                                request_query=source_step.request_query,
                                request_body=source_step.request_body,
                                response_source=source_step.response_source,
                                response_type=source_step.response_type,
                                post_var=source_step.post_var,
                                assert_var=source_step.assert_var,
                                remark="copy %s" % copy_step_name)
            copy_step = get_object_or_404(Step, name=copy_step_name)
            try:
                # 将复制的步骤和复制的用例关联
                CaseStep.objects.create(case_id=target_case_id, step_id=copy_step.id)
                msg += "<info> 复制步骤成功， 步骤名称:{}\n".format(copy_step_name)
            except Exception as e:
                msg += "<error> 复制步骤失败， 步骤名称:{}\n".format(copy_step_name)
                raise e
        msg += "<info> 成功复制用例：《%s》>>《%s》\n" % (source_case_name, target_case_name)
        print(msg)
        return msg, True


def copy_groups():
    # path = 'e:/2.txt'
    # f = open(path, 'r')
    # str_info = f.read()
    # f.close()
    # src = '批发管理-批发日报'
    # list_menu = create_menu_list(str_info)
    # for dict_menu in list_menu:
    #     if dict_menu.get("menu_action") != "commonCx":
    #         continue
    #     dec = dict_menu.get("group_name")
    #     if copy_group(src, dec):
    #         update_group_info(str_info)
    return True


def update_group_info(str_info):
    config = get_object_or_404(Config, status=True)
    # 解析从菜单请求返回的信息
    if config.auto_tag:
        print("<warning> 当前环境配置已开启auto_tag,系统将自动启用/禁用相关用例组")
    dict_menu = create_menu_dict(str_info)
    # 获取所有的用例组
    list_group = Group.objects.all()
    for group in list_group:
        if group.is_init:
            # 初始用例组不用处理
            continue
        # 如果用例组的名称不是erp的菜单名称则无需往下执行
        if group.name not in dict_menu:
            if config.auto_tag and group.status :
                print("<warning> 当前环境不存在此菜单，将该用例组禁用：%s\n" % group.name)
                group.status = False
                group.save()
            continue
        if config.auto_tag and not group.status:
            print("<warning> 当前环境存在此菜单，将该用例组启用：%s\n" % group.name)
            group.status = True
            group.save()
        #  查找用例组设置的前置变量中菜单id，如果没有设置则无需往下执行
        group_menu_id = re.findall(r'"logmenuid": "(.*?)"', group.preVar)
        if not group_menu_id:
            group_menu_id = re.findall(r'"logmenuid":"(.*?)"', group.preVar)
        if not group_menu_id:
            continue
        group_menu_id = group_menu_id[0]
        # 如果前置变量设置的菜单id与菜单请求解析的菜单id一致则无需更新
        if group_menu_id == dict_menu.get(group.name):
            continue
        # 如果前置变量设置的菜单id与菜单请求返回的id不一样则更新菜单id
        group.preVar = group.preVar.replace(group_menu_id, dict_menu.get(group.name))
        group.save()


def create_menu_dict(menu_info):
    list_f1 = StringHandler.string_to_json(menu_info)
    dict_menu = {}
    for dict_f1 in list_f1:
        f1_name = dict_f1['text']
        list_f2 = dict_f1['children']
        for dict_f2 in list_f2:
            f2_name = f1_name+'-'+dict_f2['text']
            if dict_f2.get('leaf'):
                dict_menu[f2_name] = dict_f2['id']
            else:
                list_f3 = dict_f2['children']
                for dict_f3 in list_f3:
                    f3_name = f2_name+"-"+dict_f3['text']
                    dict_menu[f3_name] = dict_f3['id']
    return dict_menu


def form_to_dict(str_form):
    list_a = []
    list_b = []
    try:
        list_str_data = str_form.split("\n")
        for sub_str_data in list_str_data:
            list_c = sub_str_data.split("\t")
            if len(list_c) < 2:
                continue
            list_a.append(list_c[0])
            list_b.append(list_c[1])
        dict_aaa = dict(zip(list_a, list_b))
        str_aaa = str(dict_aaa)
        loads = yaml.load(str_aaa.replace(":", ": "))
        result = json.dumps(loads, indent=4, sort_keys=False, ensure_ascii=False)
        result = result.replace("\\r", "").replace("\\", "")
        return result
    except Exception:
        return "数据格式错误"


