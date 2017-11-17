# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from sign.models import *
from tool.handle_case import CaseHandler
from tool.handle_group_case import GroupCaseHandler
from tool import create_case
import threading
from time import sleep,ctime


@login_required
def run_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    try:
        case_handler = CaseHandler(case_id)
        case_handler.run_case()
    except Exception:
        case.result = False
        case.msg = '初始化失败,用例未执行'
        case.save()
    return HttpResponseRedirect('/case_manage/')


def run_init_group():
    init_group = Group.objects.filter(is_init=True, status=True)[0]
    group_id = init_group.id
    group = get_object_or_404(Group, id=group_id)
    group.result =True
    group.msg = ''
    group.save()
    init_group_case_list = GroupCase.objects.filter(group_id=group_id, status=True)
    GroupCaseHandler()
    for init_group_case in init_group_case_list:
        init_case = Case.objects.get(id=init_group_case.case_id)
        if not init_case.status:
            continue
        if init_case.name == '初始化用例':
            pass
        case_id = init_case.id
        if init_case:
            GroupCaseHandler.run_case(group_id, case_id)


@login_required
def run_group_case(request, group_id, case_id):
    run_init_group()
    try:
        case_handler = GroupCaseHandler.run_case(group_id, case_id)
        case_handler.run_case()
    except Exception:
        pass
    case_list = Case.objects.filter(id=case_id)
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    username = request.session.get('username', '')
    return render(request, "group_case_manage.html", {"user": username,
                                                      "cases": case_list,
                                                      'group_id': group_id,
                                                      'group_name': group_name})


@login_required
def run_group(request, group_id):
    run_init_group()
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    case_list = []
    group_case_list = GroupCase.objects.filter(group_id=group_id, status=True)
    for group_case in group_case_list:
        case_id = group_case.case_id
        try:
            case = get_object_or_404(Case, id=case_id)
            case_list.append(case)
            if not group.is_init and group.status:
                group.result = True
                group.msg = ''
                group.save()
                GroupCaseHandler.run_case(group_id, case_id)
        except Exception:
            continue
    username = request.session.get('username', '')
    group_list = Group.objects.filter(id=group_id)
    return render(request, "group_manage.html",
                  {"user": username, "groups": group_list})
    # return render(request, "group_case_manage.html", {"user": username,
    #                                                   "cases": case_list,
    #                                                   'group_id': group_id,
    #                                                   'group_name': group_name})


@login_required
def run_whole_case(request, case_mode):
    run_init_group()
    group_case_list = GroupCase.objects.filter(status=True)
    for group_case in group_case_list:
        group_id = group_case.group_id
        case_id = group_case.case_id
        try:
            group = get_object_or_404(Group, id=group_id)
        except Exception:
            continue
        if group.is_init or not group.status:
            continue
        try:
            case = get_object_or_404(Case, id=case_id)
        except Exception:
            continue
        if case_mode == 'e' and case.result:
            continue
            # 如果是《写》用例，但是要求是只读，则跳过
        elif case_mode == 'r' and case.type == 'write':
            continue
        elif case_mode == 'w' and case.type == 'read':
            continue
        try:
            group.result = True
            group.save()
            GroupCaseHandler.run_case(group_id, case_id)
        except Exception as e:
            print(e)
            print("<warning> 当前用例失败，继续执行下一个用例")
            continue
    return HttpResponseRedirect('/whole_manage/')


@login_required
def copy_groups(request):
    try:
        create_case.copy_groups()
    except Exception as e:
        return HttpResponse('fail: {}'.format(e))
    return HttpResponse('ok')


@login_required
def copy_group(request):
    username = request.session.get('username', '')
    source = request.POST.get("group_source", "")
    target = request.POST.get("group_target", "")
    try:
        result = create_case.copy_group(source, target)
        msg = result[0]
        tag = result[1]
    except Exception as e:
        msg = '复制失败：\n{}'.format(e)
        tag = False
    return render(request, "copy_manage.html",
                  {"user": username, 'msg': msg, 'tag': tag,'source_group':source, 'target_group':target})


@login_required
def copy_case(request):
    username = request.session.get('username', '')
    source = request.POST.get("case_source", "")
    target = request.POST.get("case_target", "")
    try:
        result = create_case.copy_case(source, target)
        msg = result[0]
        tag = result[1]
    except Exception as e:
        msg = '《{0}》>>《{1}》\n复制失败：\n\t{2}'.format(source, target, e)
        tag = False
    return render(request, "copy_manage.html",
                  {"user": username, 'msg': msg, 'tag': tag,'source_case':source,'target_case':target})


@login_required
def change_form_to_dict(request):
    username = request.session.get('username', '')
    source = request.POST.get("source", "")

    result = create_case.form_to_dict(source)
    result = result.replace("\r", "")
    return render(request, "data_to_dict.html",
                  {"user": username, 'source': source, 'result': result})


def run_thread_case(thread_num, interval_time, group_name, case_name):
        run_init_group()
        print(u'<info> 并发操作开始时间: %s' % ctime())
        threads = []
        try:
            group = get_object_or_404(Group, name=group_name)
            case = get_object_or_404(Case, name=case_name)
            group_id = group.id
            case_id = case.id
        except Exception:
            return False
        try:
            # 创建线程
            for i in range(thread_num):
                t = threading.Thread(target=GroupCaseHandler.run_case, args=(group_id, case_id))
                threads.append(t)
            # 开始线程
            for i in range(thread_num):
                # 休眠间隔时间再启动
                sleep(interval_time)
                threads[i].start()
            # 等待线程结束
            for i in range(thread_num):
                threads[i].join()
            print(u'<info> 并发操作结束时间: %s' % ctime())
        except Exception as e:
            print(u"<error> 并发操作失败\n"
                  u"        %s" % e)


@login_required
def enable_all_cases():
    Case.objects.all().update(status=True)


@login_required
def disable_all_cases():
    Case.objects.all().update(status=False)


@login_required
def enable_write_cases():
    Case.objects.all().update(status=True)


@login_required
def disable_write_cases():
    Case.objects.all().update(status=False)


# @login_required
# def create_case(request):
#     try:
#         if level == '2':
#             create_second_report()
#         return HttpResponse("ok")
#     except Exception as e:
#         print(e)
#         return HttpResponse("fail! cause: {}".format(e))