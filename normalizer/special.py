"""
@Descripttion:
@Author: Markus
@Date: 2020-04-17 10:38:00
@LastEditors: Markus
@LastEditTime: 2020-04-17 17:13:08
"""

import re

from normalizer.basic_util import (
    val_num_to_chn,
    NumberSystem
)
from normalizer.normalizer import Normalizer


class Special(Normalizer):
    def __init__(self):
        self._fraction_re = re.compile(r"((\d+/\d+))")  # 这里需要写两层括号
        self._percentage_re = re.compile(r"(\d+(\.\d+)?%)")
        self._ratio_re = re.compile(r"((\d+:\d+))")
        self.system = NumberSystem()

    def normalize(self, text):
        text = self._fraction_normalize(text)
        text = self._percentage_normalize(text)
        text = self._ratio_normalize(text)
        return text

    def _fraction_normalize(self, text):
        matchers = self._fraction_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher[0]
                numerator, denominator = target.split('/')
                target = val_num_to_chn(denominator, self.system) + '分之' + \
                         val_num_to_chn(numerator, self.system)
                text = text.replace(matcher[0], target)
        return text

    def _ratio_normalize(self, text):
        matchers = self._ratio_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher[0]
                numerator, denomiator = target.split(':')
                target = val_num_to_chn(numerator, self.system) + '比' + \
                         val_num_to_chn(denomiator, self.system)
                text = text.replace(matcher[0], target)
        return text

    def _percentage_normalize(self, text):
        matchers = self._percentage_re.findall(text)
        if matchers:
            for matcher in matchers:
                target = matcher[0]
                target = '百分之' + val_num_to_chn(target.strip().strip('%'),
                                                self.system)
                text = text.replace(matcher[0], target)
        return text


if __name__ == '__main__':
    print(Special().normalize('65.3%'))
    print(Special().normalize('2135/7230'))
    print(Special().normalize('10:10'))
