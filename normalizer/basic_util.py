#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Type


class ChUnit:
    """ 读法单位 """
    def __init__(self, power, simplified):
        self.power = power
        self.simplified = simplified

    def __str__(self):
        return '10^{}'.format(self.power)


class ChDigit:
    """ 中文数字字符 """
    def __init__(self, value, simplified):
        self.value = value
        self.simplified = simplified

    def __str__(self):
        return str(self.value)


class ChMath:
    """ 中文小数点 """
    def __init__(self, symbol, simplified):
        self.symbol = symbol
        self.simplified = simplified
        return


class NumberSystem:
    def __init__(self):
        power = [1, 2, 3, 4, 8]
        simplified = [s for s in '十百千万亿']
        self.units = [ChUnit(i, v) for i, v in zip(power, simplified)]
        nums = '零一二三四五六七八九'
        self.digits = [ChDigit(i, v) for i, v in enumerate(nums)]
        self.point = ChMath('.', '点')
        return

default_sys = NumberSystem()

def __get_value(value_str, system):
    """ 使用迭代方法，计算数值和对应单位
  eg: 10260.03 -> [1, 10^4, 2, 10^2, 6, 10^1, 点, 0, 3]

  """
    striped_string = value_str.lstrip('0')
    if not striped_string:
        return []
    elif len(striped_string) == 1:
        return [system.digits[int(striped_string)]]
    else:
        result_unit = next(u for u in reversed(system.units)
                           if u.power < len(striped_string))
        result_string = value_str[:-result_unit.power]
        return __get_value(result_string,
                           system) + [result_unit] + __get_value(
                               striped_string[-result_unit.power:], system)


def seq_num_to_chn(number_string, system=None):
    """ 序列数字转成对应读法
    eg: 1234 -> 一二三四(序列型读法)

    Args:
      number_string: 字符串型数字
      system: 数字读音系统

    Returns:
      str
    """
    if system is None:
        system = default_sys
    if not isinstance(system, NumberSystem):
        raise TypeError('system should be instance of NumberSystem')
    int_string = number_string
    result_symbols = [system.digits[int(c)] for c in int_string]
    result = ''.join([s.simplified for s in result_symbols])
    return result


def val_num_to_chn(number_string, system=None):
    """ 数值数字转成对应读法
    eg: 1234 -> 一千二百三十四(数值型读法)

    Args:
        number_string: 字符串型数字
        system: 数字读音系统

    Returns:
        str
    """
    if system is None:
        system = default_sys
    if not isinstance(system, NumberSystem):
        raise TypeError('system should be instance of NumberSystem')
    if number_string[0] == "-":
        return "负" + val_num_to_chn(number_string[1:], system)

    int_dec = number_string.split('.')
    if len(int_dec) == 1:
        int_string, dec_string = int_dec[0], ""
    elif len(int_dec) == 2:
        int_string, dec_string = int_dec[0], int_dec[1]
    else:
        raise ValueError(
            "invalid input with more than one dot: {}".format(number_string))

    result = num_to_mandarin(int(int_string))

    if dec_string:
        dec_symbols = [system.point]+[system.digits[int(c)] for c in dec_string]
        result += ''.join([s.simplified for s in dec_symbols])
    return result


import re
def num_to_mandarin(num):
    """
    Convert int number to mandarin in simplified Chinese.
    :param num: int
    :return: simplified Chinese string

    In [1]: num_to_mandarin(123784700200019)
    Out[1]: '一百二十三万七千八百四十七亿零二十万零一十九'

    In [2]: num_to_mandarin(30023)
    Out[2]: '三万零二十三'

    In [3]: num_to_mandarin(102)
    Out[3]: '一百零二'

    In [4]: num_to_mandarin(15)
    Out[4]: '十五'
    """
    def to_mandarin(string):
        string = re.sub('0', '零', string)
        string = re.sub('1', '一', string)
        string = re.sub('2', '二', string)
        string = re.sub('3', '三', string)
        string = re.sub('4', '四', string)
        string = re.sub('5', '五', string)
        string = re.sub('6', '六', string)
        string = re.sub('7', '七', string)
        string = re.sub('8', '八', string)
        string = re.sub('9', '九', string)
        return string

    def integrity(num):
        k_unit = ['千', '百', '十', '']
        mandarin_str = '零' * (4 - len(str(num)) % 4) + to_mandarin(str(num))
        seg_bits = [mandarin_str[4 * i:4 * (i + 1)] for i in range(len(mandarin_str) // 4)]
        cal_seg = seg_bits[::-1]

        result = []
        for seg_idx, k_seg in enumerate(cal_seg):
            mandarin = ''
            for idx, bit in enumerate(k_seg):
                if bit == '零':
                    continue
                else:
                    if k_seg[idx - 1] == '零' and mandarin:
                        mandarin += '零'
                    mandarin += bit + k_unit[idx]
            if k_seg == '零' * 4:
                mandarin = ''
            else:
                if k_seg[0] == '零':
                    try:
                        if cal_seg[seg_idx + 1]:
                            mandarin = '零' + mandarin
                    except IndexError:
                        if mandarin.startswith('一十'):
                            mandarin = mandarin.lstrip('一')

            suffix = '万' if seg_idx % 2 else '亿'
            if seg_idx == 0 or not mandarin:
                suffix = ''
            result.append(mandarin + suffix)
        return ''.join(result[::-1])
    return integrity(num) if num!=0 else '零'


if __name__ == '__main__':
    # 测试程序
    num_sys = NumberSystem()
    print()
    # print('0:', val_num_to_chn('0', num_sys))
    # print('10:', val_num_to_chn('10', num_sys))
    print('0000:', val_num_to_chn('00', num_sys))
    # print('10260.03:', val_num_to_chn('10260.03', num_sys))
    # print('1234:', val_num_to_chn('1234', num_sys))
    # print('320000:', val_num_to_chn('320000', num_sys))
    # print('123456789:', val_num_to_chn('123456789', num_sys))
    # print('-197.4:', val_num_to_chn('-197.4', num_sys))
    # print('120000:', seq_num_to_chn('120000', num_sys))
