
# -*- coding: utf-8 -*-

import traceback
import os
from normalizer.car_number import CarNumber
from normalizer.date import Date
# from cardinal import cardinal2chntext, cardinal_normalize
from normalizer.digit import digit_normalize
from normalizer.measure import Measure
from normalizer.money import Money
from normalizer.special import Special
from normalizer.symbol import Symbol
from normalizer.telephone import TelePhone
from normalizer.number import Number


class TextNormalizer:
    def __init__(self):
        pass

    def load(self, base_path=None):
        self._date = Date()
        self._money = Money()
        self._car_number = CarNumber()
        self._measure = Measure()
        self._telephone = TelePhone()
        self._special = Special()
        self._symbol = Symbol()
        self._number = Number()

    @staticmethod
    def _preprocess(text):
        text = '^' + text + '$'
        text = text.replace('％', '%')
        return text

    @staticmethod
    def _postprocess(text):
        return text.lstrip('^').rstrip('$')

    def infer(self, text):
        return self.normalize(text)

    def normalize_(self, text):
        text = self._preprocess(text)

        # 非抢占性正则
        text = self._date.normalize(text)  # 规范化日期
        text = self._money.normalize(text)
        text = self._car_number.normalize(text)  # 规范车牌
        text = self._measure.normalize(text)
        # 抢占性正则
        text = self._telephone.normalize(text)  # 规范化固话/手机号码
        # text = self._english.normalize(text)  # 规范英文
        text = self._special.normalize(text)  # 规范分数以及百分比
        text = self._number.normalize(text) # 规范化其他可能的数字
        # 通用正则
        text = digit_normalize(text)  # 规范化数字编号
        text = self._symbol.normalize(text)  # 规范化符号

        text = self._postprocess(text)
        return text

    def normalize(self, text):
        try:
            text = self._preprocess(text)
            # 非抢占性正则
            text = self._date.normalize(text)  # 规范化日期
            text = self._money.normalize(text)
            text = self._car_number.normalize(text)  # 规范车牌
            text = self._measure.normalize(text)
            # 抢占性正则
            text = self._telephone.normalize(text)  # 规范化固话/手机号码
            # text = self._english.normalize(text)  # 规范英文
            text = self._special.normalize(text)  # 规范分数以及百分比
            text = self._number.normalize(text) # 规范化其他可能的数字
            # 通用正则
            text = digit_normalize(text)  # 规范化数字编号
            text = self._symbol.normalize(text)  # 规范化符号
        except Exception:
            _log.warning(traceback.format_exc())

        text = self._postprocess(text)
        return text

if __name__ == '__main__':

    tn = TextNormalizer()
    tn.load()
    print(tn.normalize('固话：059523865596或23880880。'))
    print(tn.normalize('手机：19859213959或15659451527。'))
    print(tn.normalize('分数：32477/76391。'))
    print(tn.normalize('百分数：80.30%。'))
    print(tn.normalize('编号：31520181154418。'))
    print(tn.normalize('纯数：2983.60克或12345.60米。'))
    print(tn.normalize('日期：1999年2月20日或09年3月15号。'))
    print(tn.normalize('金钱：12块5，34.5元，20.1万'))
    print(tn.normalize('车牌：粤A7482的轿车'))
    print(tn.normalize('特殊：O2O或B2C。'))
    print(tn.normalize('邮箱：zhangyue@163.com。'))
    print(tn.normalize('其它：名字格式为：首字+尾字'))
    print(tn.normalize('奥迪A5。'))
    print(tn.normalize('给你500'))
    print(tn.normalize('黎明03：00 - 05:00'))
