# coding:utf-8
from datetime import timedelta
import datetime
import time


class TimeHandler(object):
    """时间处理器"""
    @staticmethod
    def getIntTime(bool_isMs=True):
        """
        获取整型时间
        str_type: ms表示获取到ms级别，否则获取到s级别
        """
        int_multy = bool_isMs is True and 1000 or 100
        return int(round(time.time() * int_multy))

    @staticmethod
    def getStrTime(str_format="%Y%m%d%H%M%S%f", int_relDay=0, int_relSecond=0, int_sublength=None):
        """
        获取字符型时间
        :param str_format: 时间格式，默认是%Y%m%d%H%M%S%f
        :param int_relDay: 在当天基础上的时间增量，天级别
        :param int_relDay: 在当前秒的基础上的时间增量，秒级别
        :param int_sublength: 截取长度
        :return:
        """
        time.sleep(0.1)
        now = datetime.datetime.now()
        now = now + timedelta(days=int_relDay)
        now = now + timedelta(seconds=int_relSecond)
        if int_sublength:
            return now.strftime(str_format)[0:int_sublength]
        return now.strftime(str_format)


if __name__ == "__main__":
    print(TimeHandler().getIntTime())
