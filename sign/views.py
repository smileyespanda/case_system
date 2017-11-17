# coding=utf-8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
# 首页(登录)
def index(request):
    return render(request, "index.html")


def show_init_sql(request):
    init_db_file = open("init_db.sql", "rb")
    list_sql = init_db_file.readlines()
    init_db_file.close()
    return render(request, "show_init_sql.html", {"list_sql": list_sql})


def show_app_log(request):
    init_db_file = open("app.log", "rb")
    list_log = init_db_file.readlines()
    init_db_file.close()
    return render(request, "show_app_log.html", {"list_log": list_log})


def tool(request):
    return render(request, "data_to_dict.html")


def show_img(request):
    return render(request, "img.html")


# 登录动作
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == '' or password == '':
            return render(request, "index.html", {"error": "username or password null!"})

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)   # 验证登录
            response = HttpResponseRedirect('/content_manage/')   # 登录成功跳转发布会管理
            request.session['username'] = username      # 将 session 信息写到服务器
            return response
        else:
            return render(request, "index.html", {"error": "username or password error!"})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)    # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


"""
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
"""
