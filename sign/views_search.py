# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from sign.models import *
from django.http import HttpResponseRedirect

# Create your views here.


@login_required
def search_group(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    group_list = Group.objects.filter(name__contains=search_name_bytes)
    return render(request, "group_manage.html", {"user": username, "groups": group_list})


@login_required
def search_case(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    case_list = Case.objects.filter(name__contains=search_name_bytes)
    return render(request, "case_manage.html", {"user": username, "cases": case_list})


@login_required
def search_group_case(request, group_id):
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name     # .encode(encoding="utf-8")
    username = request.session.get('username', '')
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    group_case_list = GroupCase.objects.filter(group_id=group_id)
    case_list = []
    search_case_list = []
    for group_case in group_case_list:
        case_id = group_case.case_id
        case_list.append(get_object_or_404(Case, id=case_id))
    for case in case_list:
        case_name = case.name
        if case_name.__contains__(search_name_bytes):
            search_case_list.append(case)
    return render(request, "group_case_manage.html", {"user": username,
                                                      "cases": search_case_list,
                                                      'group_id': group_id,
                                                      'group_name': group_name})


@login_required
def search_step(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    step_list = Step.objects.filter(name__contains=search_name_bytes)
    return render(request, "step_manage.html", {"user": username, "steps": step_list})


@login_required
def search_case_step(request, group_id, case_id):
    group = get_object_or_404(Group, id=group_id)
    group_name = group.name
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name
    username = request.session.get('username', '')
    case = get_object_or_404(Case, id=case_id)
    case_name = case.name
    case_step_list = CaseStep.objects.filter(case_id=case_id)
    step_list = []
    search_step_list = []
    for case_step in case_step_list:
        step_id = case_step.step_id
        step_list.append(get_object_or_404(Step, id=step_id))
    for step in step_list:
        step_name = step.name
        print(search_name_bytes)
        print(step_name)
        if step_name.__contains__(search_name_bytes):
            search_step_list.append(step)
    return render(request, "case_step_manage.html",
                  {"user": username, "steps": search_step_list,
                   "case_id": case_id, "case_name": case_name,
                   'group_id': group_id, "group_name": group_name})



