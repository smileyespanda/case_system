# coding:utf-8

import pymysql
import pyodbc
import cx_Oracle
from sign.models import *
from django.shortcuts import get_object_or_404
from tool import handle_log


class DBHandler:
    """
    数据库相关操作类
    """
    def __init__(self):
        # 设置数据库配置信息
        self.conn = None
        self.cur = None
        self.config = get_object_or_404(Config, status=True)
        self.host = self.config.dataBase_host
        self.port = self.config.dataBase_port
        self.dbName = self.config.dataBase_name
        self.user = self.config.dataBase_user
        self.pwd = self.config.dataBase_pwd
        self.dbtype = self.config.dataBase_type
        self.need_init = self.config.init_db

    def connect_db(self):
        """
        链接数据库
        :return:
        """
        if self.dbtype == "sqlServer":
            self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;'
                                       'UID=%s;PWD=%s' % (self.host, self.dbName, self.user, self.pwd))
        elif self.dbtype == "mysql":
            # mysql
            print("port is", self.port)
            self.conn = pymysql.connect(host=self.host,
                                        port=int(self.port),
                                        user=self.user,
                                        password=self.pwd,
                                        db=self.dbName,
                                        charset='utf-8',
                                        cursorclass=pymysql.cursors.DictCursor)
        else:
            dsn = cx_Oracle.makedsn(self.host, int(self.port), self.dbName)
            self.conn = cx_Oracle.connect(self.user, self.pwd, dsn)
        self.cur = self.conn.cursor()
        handle_log.build_log("<info> 成功连接数据库~")
        if not self.cur:
            handle_log.build_log("<error> 连接数据库失败,链接信息:\n"
                                 "        host:%s\n"
                                 "        port: %s\n"
                                 "        user: %s\n"
                                 "        pwd: %s\n"
                                 "        db: %s\n"
                                 % (self.host, self.port, self.user, self.pwd, self.dbName))
            raise(NameError, "连接数据库失败")

    def exec_query(self, str_sql):
        """
        执行select语句
        :param str_sql:
        :return:查询到的结果列表
        """
        try:
            cur = self.cur
            cur.execute(str_sql)
            list_result = cur.fetchall()
            return list_result
        except Exception:
            handle_log.build_log(u"<error> sql执行失败:\n"
                                 u"        sql详情：\n"
                                 u"        %s\n" % str_sql)
            raise False

    def exec_non_query(self, str_sql):
        """
        执行select以外的语句
        :param str_sql: 需要执行的sql
        :return:None
        """
        try:
            cur = self.cur
            cur.execute(str_sql)
            self.conn.commit()
        except Exception:
            handle_log.build_log("<error> sql执行失败:\n"
                                 "        sql详情：%s\n" % str_sql)
            raise False

    def close_db(self):
        """
        关闭数据库
        :return:
        """
        if self.conn:
            self.conn.close()
        handle_log.build_log("<info> 关闭数据库链接成功\n")


if __name__ == '__main__':
    config = {
        'dataBase_host': '172.16.0.233',
        'dataBase_port': '1433',
        'dataBase_name': 'LS5.3.011tyb',
        'dataBase_user': 'LsByTest',
        'dataBase_pwd': 'LsTest159357',
        'dataBase_type': '1'
    }
    dbhandler = DBHandler(config)
    dbhandler.conn = None
    dbhandler.cur = None
    dbhandler.connect_db()
    str_sql = "select tid from dm_gsxx where name='总公司';"
    rows = dbhandler.exec_query(str_sql)
    for row in rows:
        print(row[0])
