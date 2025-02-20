"""
@Descripttion:
@Author: Markus
@Date: 2020-04-10 19:51:09
@LastEditors: Markus
@LastEditTime: 2020-04-12 23:22:18
"""
import re

from normalizer.basic_util import (
    NumberSystem,
    val_num_to_chn
)
from normalizer.digit import digit_normalize
from normalizer.number import numeric_normalize
from normalizer.normalizer import Normalizer


class Date(Normalizer):
    def __init__(self):
        self.system = NumberSystem()

        month_day_pattern = r"((\d+)[月日号])"  # 用来匹配月日号前的数字
        two_year_pattern = r"([6-9]|[0,1])[0-9]年"  # 60~99年, 00~09年, 10~19年
        four_year_pattern = r"(1[0-9][0-9][0-9]|20[0-9][0-9])年"  # 1000~1999/2000～
        year_pattern = "({}|{})".format(two_year_pattern, four_year_pattern)
        month_pattern = r"((0?[1-9]|1[0-2])月)"  # (0)1~(0)9月，10~12月
        day_pattern = r"((0?[1-9]|[1-3][0-9])[日号])"  # (0)1~(0)9日/号，10~39日/号
        date_pattern = r"({0}|{1}|{2})".format(year_pattern, month_pattern,
                                               day_pattern)
        two_time_pattern = r"((20|21|22|23|[0-1]\d):[0-5]\d)"
        three_time_pattern = r"((20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d)"

        time_pattern = r"({0}|{1})".format(three_time_pattern, two_time_pattern)

        self.time_re = re.compile(time_pattern)
        self.date_re = re.compile(date_pattern)
        self.month_day_re = re.compile(month_day_pattern)

    def normalize(self, text):
        text = text.replace('：', ':')
        matchers = self.date_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher[0]
                # print(target)
                target, flag = self._date_num_normalize(target)
                if flag:
                    target = digit_normalize(target)
                else:
                    target = numeric_normalize(target)
                text = text.replace(matcher[0], target)
        matchers = self.time_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher[0]
                target = self._time_num_normalize(target)
                text = text.replace(matcher[0], target)
        return text

    def _time_num_normalize(self, text):
        nums = text.split(':')
        text = ""
        if nums[0] == '00':
            h = '零'
        else:
            h = val_num_to_chn(nums[0], self.system)
        if h == '二':
            h = '两'
        text += (h + '点')
        if len(nums) == 2:
            if nums[1] == '00':
                # text += '整'
                pass
            else:
                m = val_num_to_chn(nums[1], self.system)
                if nums[1][0] == '0':
                    m = '零' + m
                text += (m + '分')
        else:
            if nums[1] == '00' and nums[2] == '00':
                # text += '整'
                pass
            else:
                if nums[1] == '00':
                    m = '零'
                else:
                    m = val_num_to_chn(nums[1], self.system)
                if nums[1][0] == '0':
                    m = '零' + m
                if nums[2] == '00':
                    text += (m + '分')
                else:
                    s = val_num_to_chn(nums[2], self.system)
                    if nums[2][0] == '0':
                        s = '零' + s
                    text += (m + '分' + s + '秒')
        return text

    def _date_num_normalize(self, text):
        matchers = self.month_day_re.findall(text)
        # flag: 内容是否为年份
        flag = True
        if matchers:
            flag = False
            for matcher in matchers:
                target = matcher[0]
                target = target.lstrip('0')
                text = text.replace(matcher[0], target)
        return text, flag


if __name__ == '__main__':
    print(Date().normalize('今年是09年3月16日啊'))
    print(Date().normalize('今年是09年03月31日啊'))
    print(Date().normalize('今年是3月20日啊'))
    print(Date().normalize('3月20日'))
    print(Date().normalize('1929年'))

    print(Date().normalize("现在是09年3月16日19:20:30"))
    print(Date().normalize("现在是09年3月16日19:01"))
