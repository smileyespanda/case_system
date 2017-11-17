# # coding:utf-8
# from django.shortcuts import get_object_or_404
# from sign.models import *
# from tool.handle_case import CaseHandler
# from tool.handle_group_case import GroupCaseHandler
#
#
# class GroupHandler(object):
#     def __init__(self, group_id):
#         self.group_id = group_id
#
#     def run_group(self):
#         group = Group.objects.get(id=self.group_id, status=True)
#         group.result = True
#         group.save()
#         print(u"<info> **************开始执行用例组********************\n")
#         print(u"<info> id：%d; name：%s\n" % (group.id, group.name))
#         group_case_list = GroupCase.objects.filter(group_id=self.group_id, status=True)
#         for group_case in group_case_list:
#             case_id = group_case.case_id
#             try:
#                 GroupCaseHandler(self.group_id, case_id)
#             except Exception:
#                 continue
#
#
#
#
#
#
