from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import logging
from tool.handle_group_case import GroupCaseHandler


@login_required
def whole_manage(request):
    group_list = Group.objects.filter(result=False, status=True)
    username = request.session.get('username', '')
    return render(request, "whole_manage.html", {"user": username, 'groups': group_list})


@login_required
def group_manage(request):
    group_list = Group.objects.all()
    if len(group_list) > 20:
        group_list = group_list[0:15]
    username = request.session.get('username', '')
    return render(request, "group_manage.html",
                  {"user": username, "groups": group_list})


@login_required
def single_group_manage(request, group_id):
    group_list = Group.objects.filter(id=group_id)
    username = request.session.get('username', '')
    return render(request, "group_manage.html",
                  {"user": username, "groups": group_list})


@login_required
def group_case_manage(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    group_case_list = GroupCase.objects.filter(group_id=group_id)
    case_list = []
    for group_case in group_case_list:
        case_id = group_case.case_id
        case_list.append(get_object_or_404(Case, id=case_id))
    username = request.session.get('username', '')
    return render(request, "group_case_manage.html", {"user": username,
                                                      "cases": case_list,
                                                      'group_id': group_id,
                                                      'group_name': group_name})


@login_required
def case_manage(request):
    case_list = Case.objects.all()
    # case_list = []
    username = request.session.get('username', '')
    return render(request, "case_manage.html",
                  {"user": username, "cases": case_list})


@login_required
def case_step_manage(request, group_id, case_id):
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    case = get_object_or_404(Case, id=case_id)
    case_name = case.name
    case_step_list = CaseStep.objects.filter(case_id=case_id)
    step_list = []
    for case_step in case_step_list:
        step_id = case_step.step_id
        step_list.append(get_object_or_404(Step, id=step_id))
    username = request.session.get('username', '')
    return render(request, "case_step_manage.html",
                  {"user": username, "steps": step_list,
                   "case_id": case_id, "case_name": case_name,
                   'group_id': group_id, "group_name": group_name})


@login_required
def step_manage(request):
    step_list = Step.objects.all()
    username = request.session.get('username', '')
    return render(request, "step_manage.html", {"user": username, "steps": step_list})


@login_required
def config_manage(request):
    group_list = Group.objects.all()
    for group in group_list:
        case_list = Case.objects.filter(group_id=group.id)
        group.size = len(case_list)
        group.save()
    username = request.session.get('username', '')
    return render(request, "group_manage.html", {"user": username, "groups": group_list})


@login_required
def content_manage(request):
    username = request.session.get('username', '')
    return render(request, "content_manage.html", {"user": username})


@login_required
def copy_manage(request):
    tag = True
    username = request.session.get('username', '')
    return render(request, "copy_manage.html",
                  {"user": username, 'msg': '', 'tag': tag})