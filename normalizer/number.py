"""
Description:
Company: Bilibili Inc.
Version:
Author: Xie Chang
Date: 2021-08-04 15:06:22
LastEditors: Xie Chang
LastEditTime: 2021-08-05 22:28:26
"""

import re

from normalizer.basic_util import (
    val_num_to_chn,
    NumberSystem
)

from jieba import posseg as psg
from normalizer.normalizer import Normalizer

float_number_pattern = r"\d+\.\d+"
decimal_pattern = r"\d+"

key_word_set = {
    '价',
    '量'
}

class Cardinal(Normalizer):
    def __init__(self) -> None:
        self.system = NumberSystem()

    def normalize(self, text):
        target = val_num_to_chn(text, self.system)
        return target


class Number(Normalizer):
    def __init__(self, direct=False) -> None:
        self.system = NumberSystem()
        self.float_number_re = re.compile(float_number_pattern)
        self.decimal_re = re.compile(decimal_pattern)
        self.psg = psg
        self.psg.lcut("hehe")
        self.direct = direct

    def normalize(self, text):
        if self.direct:
            return val_num_to_chn(text, self.system)
        # 带小数点的默认按照数值读法进行正则化
        matchers = self.float_number_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher
                target = val_num_to_chn(target, self.system)
                text = text.replace(matcher, target)
        # 整型数据目前尝试根据上下文判断
        # matchers = self.decimal_re.finditer(text)
        matcher = self.decimal_re.search(text)
        while matcher:
            index = matcher.span()
            target = matcher.group()
            start, end = index
            if len(target) == 2:
                # 两位孤立数字(长度等于2且相邻字符非英文) 默认用数值读法
                start = start - 1
                flag = True
                if start >= 0 and text[start].encode('utf-8').isalpha():
                    flag = False
                if end < len(text) and text[end].encode('utf-8').isalpha():
                    flag = False
                if flag:
                    target = val_num_to_chn(target, self.system)
                    text = text[:index[0]] + target + text[index[1]:]
                    # text = text.replace(matcher[0], target)
            elif len(target) == 1 or len(target) >= 5:
                pass
            else:
                # 上文推断
                begin = max(start - 5, 0)
                context = text[begin:start]
                flag = False
                for word in key_word_set:
                    if word in context:
                        flag = True
                        break
                if not flag:
                    result = self.psg.lcut(context)
                    # print(result)
                    for item in result[:-1]:
                        if item.flag == 'v':
                            flag = True
                            break
                    if result[-1].flag == 'r':
                        flag = True
                if flag:
                    target = val_num_to_chn(target, self.system)
                    if len(target) == 2 and target[0] == '二' and target[1] != '十':
                        target = '两' + target[1:]
                    # text = text.replace(matcher[0], target)
                    text = text[:index[0]] + target + text[index[1]:]
            matcher = self.decimal_re.search(text, pos=index[1])
        return text


def numeric_normalize(text):
    pattern = re.compile(r"((\d+))")
    matchers = pattern.findall(text)
    if matchers:
        for matcher in matchers:
            target = matcher[0]
            target = val_num_to_chn(target)
            text = text.replace(matcher[0], target)
    return text


if __name__ == '__main__':
    print(Number().normalize('衬衫的价格是9.15元，编号是12'))
    print(Number().normalize('航班号是CA85U9'))
