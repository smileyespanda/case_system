# coding:utf-8
import random
import re
from bs4 import BeautifulSoup


class StringHandler(object):
    """字符串处理器"""
    @staticmethod
    def get_str_mix_digital(int_size):
        """
        获取字母和数字组合的混合字符串
        :param int_size: 字符串的长度
        :return: 混合字符串
        """
        str_mix = ""
        for i in range(int_size):
            s_type = random.randrange(10)
            r_type = s_type % 2 == 0 and "char" or "int"
            if r_type == "char":
                str_mix += chr(random.randrange(65, 90))
            else:
                str_mix += str(random.randrange(1, 9))
        return str_mix

    @classmethod
    def get_middle_str_list(cls, original_str, start_str, end_str):
        """
        获取字符串中以start_str开头，以end_str结尾的字符串数组
        :param original_str: 原始字符串
        :param start_str: 字符串前缀
        :param end_str: 字符串后缀
        :return: 以start_str开头，以end_str结尾的字符串数组
        """
        list_middle_str = []
        new_str = original_str
        while True:
            mid_str = cls.get_middle_str(new_str, start_str, end_str)
            if mid_str == "":
                break
            list_middle_str.append(mid_str)
            start_index = new_str.find(mid_str)
            start_index += len(mid_str)+len(end_str)
            new_str = new_str[start_index:]
        return list_middle_str

    @classmethod
    def get_middle_str(cls, original_str, start_str="", end_str=""):
        """
        获取字符串中第一个以start_str开头，以end_str结尾的字符串
        :param original_str:原始字符串
        :param start_str:字符串前缀
        :param end_str:字符串后缀
        :return:一个以start_str开头，以end_str结尾的字符串
        """
        middle_str = ""
        start_index = original_str.find(start_str, 0)
        if start_index >= 0:
            start_index += len(start_str)
            new_str = original_str[start_index:]
            end_index = new_str.find(end_str, 0)
            if end_index >= 0:
                end_index += start_index
                middle_str = original_str[start_index:end_index]
        return middle_str

    @staticmethod
    def is_contain(str_text, str_sub_text, bool_sensitive=True):
        """
        父字符串str_text是否包含子字符串str_sub_text
        :param str_text:父字符串
        :param str_sub_text:子字符串
        :param bool_sensitive: 大小写敏感
        :return:
        """
        if not bool_sensitive:
            str_text = str_text.lower()
            str_sub_text = str_sub_text.lower()
        return str_text.__contains__(str_sub_text)

    @staticmethod
    def is_equal(str_text1, str_text2, bool_sensitive=True):
        """
        字符串str_text1是否包含字符串str_text2是否相等
        :param str_text1:父字符串
        :param str_text2:子字符串
        :param bool_sensitive: 大小写敏感
        :return:
        """
        if not bool_sensitive:
            str_text1 = str_text1.lower()
            str_text2 = str_text2.lower()
        return str_text1 == str_text2

    @staticmethod
    def contain_chinese(str_text):
        """判断str_text是否含有中文"""
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zh_pattern.search(str_text)
        return bool(match)

    @classmethod
    def string_to_json(cls, str_json):
        id = "id"
        ckdm = "id"
        true = True
        false = False
        result = True
        i = 0
        try:
            while(1):
                if i > 20:
                    break
                try:
                    list_info = eval(str_json)
                    return list_info
                except NameError as e:
                    i += 1
                    var = cls.get_middle_str(e.args[0], "'", "'")
                    locals()[var] = var
        except Exception:
            print("<error> 字符串转化为json出错\n"
                  "        字符串详情：%s\n" % str_json)


    @classmethod
    def get_string_attr(cls, str_text, str_type="html", list_find_info=[]):
        """
        获取字符串中的变量属性
        :param str_text:
        :param str_type:
        :param list_find_info:
        :return:
        """
        str_type = str_type.lower()
        attr_value = None
        try:
            if str_type == "html":
                attr_value = cls.get_str_html_attr(str_text, list_find_info)
            elif str_type == "json":
                attr_value = cls.get_str_json_attr(str_text, list_find_info)
            elif str_type == "string":
                attr_value = cls.get_str_str_attr(str_text, list_find_info)
            return attr_value
        except Exception:
            # print(u"<error> %s\n" % e)
            raise False

    @classmethod
    def get_str_str_attr(cls, str_str, list_find_info):
        try:
            attr_index = None
            try:
                start_index = list_find_info[0]
                end_index = list_find_info[1]
                if len(list_find_info) > 2:
                    attr_index = int(list_find_info[2])
            except Exception:
                print(u"<error> 表达式格式错误\n")
                raise False
            list_attr = cls.get_middle_str_list(str_str, start_index, end_index)
            # 如果指定索引则返回索引对应的值，否则返回所有找到的值
            if attr_index is None:
                attr_value = ",".join(list_attr)
            else:
                try:
                    attr_value = list_attr[attr_index]
                except Exception:
                    print(u"<error> 索引溢出\n")
                    raise False
            return attr_value
        except Exception:
            raise False

    @classmethod
    def get_str_html_attr(cls, str_html, list_find_info):
        """
        获取页面属性值，key为属性名称，value为属性值
        :param str_html: 页面源代码
        :param list_find_info: [属性种类,属性名称]
        :return:属性对字典
        """
        try:
            attr_type = list_find_info[0]
            attr_name = list_find_info[1]
            attr_index = None
            if len(list_find_info) > 2:
                attr_index = int(list_find_info[2])
            attr_value = cls.get_html_attr(str_html, attr_type, attr_name, attr_index)
            return attr_value
        except Exception:
            # print(u"<error> 获取页面属性失败:\n"
            #       u"        html文本：%s\n"
            #       u"        属性查找信息：%s"
            #        % (str_html, ",".join(list_find_info)))
            raise False

    @classmethod
    def get_html_attr(cls, str_html, attr_type, attr_name, attr_index=None):
        """
        获取页面属性值，key为属性名称，value为属性值
        :param str_html: 页面源代码
        :param attr_type: 属性种类,属性名称
        :param attr_name: 属性名称
        :param attr_index: 属性索引,默认为0
        :return:属性对字典
        """
        try:
            html_obj = BeautifulSoup(str_html, "html.parser")
            list_attr = html_obj.find_all(attrs={attr_type: attr_name})
            if not list_attr:
                raise None
            # 如果不指定索引就返回所有查到的数据
            list_attr_value = []
            for attr in list_attr:
                list_attr_value.append(attr.get("value"))
            if attr_index is None:
                attr_value = ",".join(list_attr_value)
            else:
                attr_value = list_attr_value[attr_index]
            return attr_value
        except Exception:
            print(u"<error> 查找html属性失败:\n"
                  u"        属性类型：%s\n"
                  u"        属性名称：%s\n" % (attr_type, attr_name))
            raise False

    @classmethod
    def get_html_tag(cls, str_html, tag_name, tag_index=0):
        """
        获取页面属性值，key为属性名称，value为属性值
        :param str_html: 页面源代码
        :param tag_name: 标签名称
        :param tag_index: 标签索引，默认是第一个
        :return:属性对字典
        """
        try:
            html_obj = BeautifulSoup(str_html, "lxml")
            tag = html_obj.find_all(tag_name)
            tag_value = str(tag[tag_index])
            return tag_value
        except Exception:
            print(u"<error> 查找html标签失败:\n"
                  u"        标签类型：%s\n"
                  u"        标签索引：%s\n" % (tag_name, tag_index))
            raise False

    @classmethod
    def get_str_json_attr(cls, str_json, list_finds):
        """
        查找json属性值
        :param str_json: json字符串
        :param list_finds: 查找信息列表，有几层则传几个参数
        :return:
        """
        try:
            json_obj = cls.string_to_json(str_json)
            json_obj_new = json_obj
            for str_find in list_finds:
                list_info = str_find.split("-")
                json_obj_new = cls.find_json_attr(json_obj_new, list_info)
            json_attr = json_obj_new
            return json_attr
        except Exception:
            print(u"<error> 获取json串(字符串)属性失败: \n"
                  u"        查找信息：%s\n" % (",".join(list_finds)))
            raise False

    @classmethod
    def find_json_attr(cls, json_obj, list_info):
        """
        查找json属性值
        :param json_obj: json对象
        :param list_info:查找的属性/定位属性-定位的属性值-查找的属性,实例["name"]、["name-cname-id"]
        :return:
        """
        json_attr = None
        try:
            for sub_json_obj in json_obj:
                if not sub_json_obj:
                    continue
                if len(list_info) == 1:
                    json_attr = sub_json_obj[list_info[0]]
                    break
                if sub_json_obj[list_info[0]] == list_info[1]:
                    json_attr = sub_json_obj[list_info[2]]
                    break
        except Exception:
            if len(list_info) == 1:
                json_attr = json_obj[list_info[0]]
            else:
                if json_obj[list_info[0]] == list_info[1]:
                    json_attr = json_obj[list_info[2]]
        finally:
            return json_attr

    @classmethod
    def string_to_dict(cls, str_dict):
        try:
            if str_dict:
                return eval(str_dict)
            return {}
        except Exception:
            print(u"<error> 数据格式错误:\n"
                  u"        %s" % str_dict)
            raise False

    @classmethod
    def encode_dict(cls, dict_data):
        for k,v in dict_data.items():
            dict_data[k] = v.encode("gbk")
        return dict_data


if __name__ == "__main__":
    SH = StringHandler()
    str_a = 'xxxaaayyyxxxbbbyyy'
    print(SH.get_middle_str_list(str_a, '"', '"'))
