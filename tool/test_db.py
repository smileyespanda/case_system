# coding:utf-8
import pyodbc

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.0.233;DATABASE=LS5.3.011tyb;UID=LsByTest;PWD=LsTest159357')
cur = conn.cursor()
str_sql = "select tid from dm_gsxx where name='总公司';"
cur.execute(str_sql)
rows = cur.fetchall()
for row in rows:
    print(row[0])
# import pymssql
# conn = pymssql.connect(host='172.16.0.233', port='1433', user='LsByTest',
#                        password='LsTest159357', database='LS5.3.011tyb', charset="utf8")
# cur = conn.cursor()
# cur.execute("select tid from dm_gsxx where name='总公司';")
# rows = cur.fetchall()
# for row in rows:
#     print(row[0])

# import cx_Oracle
#
# dsn = cx_Oracle.makedsn("172.16.199.33", 1521, "gyltest")
# conn = cx_Oracle.connect("supply", "chain", dsn)
# curs = conn.cursor()
# sql = 'select entityid from companyinfo'
# rr = curs.execute(sql)
# rows = curs.fetchall()
# print(rows)
# curs.close()
# conn.close()


# import pymysql
# conn = pymysql.connect(host="127.0.0.1", port=3306, database="test_db", user="root", password="")
# cur = conn.cursor()
# cur.execute("select * from auth_user;")
# rows = cur.fetchall()
# print(rows)
# cur.close()
# conn.close()

# import requests
# from tool.handle_string import StringHandler
# r = requests.session()
#
# wn_url = 'http://wc.139erp.com/index.html'
# yzm_url = 'http://www.139erp.com/web/jsp/image.jsp'
# gsdm_url = 'http://www.139erp.com/indexjs.jsp'
# puser = 'sz'
# ppwd = 'hzby!2016'
# luser = 'by'
# lpwd = 'byls01HK%9a'
#
# logdata = {
#     # "gsDm": "26280",
#     "loginName": "sz",
#     "password": "hzby!2016",
#     "yzm": "2302",
#     "fullhardware": "77921cb0977197808f00b204e980099834cf8c08dd18eee99",
#     "hardware": "77921cb0977197808f00b204e980099834cf8c08dd18eee99",
#     "addrName": "",
#     "MacByNetbios": "D4-3D-7E-35-74-8C",
#     "HardDisk": "000000",
#     "IntelCpu": "000306A9-00000000-00000000",
#     "HardDriveID": "600000000",
#     "crm_url": "http: //bd.139erp.com: 2880/crm"
# }
#
# def get_erp_url(gsdm):
#     gsdm = int(gsdm)
#     r.get(wn_url)
#     res = r.get(yzm_url)
#     yzm = StringHandler.get_middle_str(res.headers['Set-Cookie'], "byszx_login=", ";")
#     logdata["yzm"] = yzm
#     res = r.get(gsdm_url).text
#     res = StringHandler.get_middle_str(res, "szGsxx=", ";")
#     url_dict_list = StringHandler.string_to_json(res)
#     for url_dict in url_dict_list:
#         start = url_dict.get("start")
#         end = url_dict.get("end")
#         if int(start) <= gsdm and int(end) >= gsdm:
#             return url_dict.get("url")
#     return None
#
# def login(gsdm, type):
#     erp_url = get_erp_url(gsdm)
#     logdata["gsDm"] = str(gsdm)
#     if not erp_url:
#         return "您输入的公司代码不存在"
#     if type.lower() == "ls":
#         logdata["loginName"] = luser
#         logdata["password"] = lpwd
#     login_url = erp_url + "/login.action?frameChannel=true"
#     res = r.post(url=login_url, data=logdata)
#     print(res.text)
#     r.get(erp_url + "/simplepf.action?swlx=S&&crkfs=PF&logmenuid=521&logmenuname=%C5%FA%B7%A2&gsdm=26280&username=by")
#
#
# login('26280', 'pf')