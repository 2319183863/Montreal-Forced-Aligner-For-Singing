# -*- coding: utf-8 -*-
"""DIGIT类

"""

import re
from LeTTS.text.chinese.normalizer.basic_util import (
    seq_num_to_chn,
    NumberSystem
)
from LeTTS.common.types.word import Word
from LeTTS.common.enum.rhythm import Rhythm
from LeTTS.text.chinese.normalizer.normalizer import Normalizer

class Characters(Normalizer):
    def __init__(self) -> None:
        self.system = NumberSystem()
        phonemes ={
            "0":'ling1',
            "1":'yi1',
            "2":'er4',
            "3":'san1',
            "4":'si4',
            "5":'wu3',
            "6":'liu4',
            "7":'qi1',
            "8":'ba1',
            "9":'ba1',
            "a":'EY1',
            "b":'B IY1',
            "c":'S IY1',
            "d":'D IY1',
            "e":'IY1',
            "f":'EH1 F',
            "g":'JH IY1',
            "h":'EY1 CH',
            "i":'AY1',
            "j":'JH EY1',
            "k":'K EY1',
            "l":'EH1 L',
            "m":'EH1 M',
            "n":'EH1 N',
            "o":'OW1',
            "p":'P IY1',
            "Q":'K Y UW1',
            "r":'AA1 R',
            "s":'EH1 S',
            "t":'T IY1',
            "u":'Y UW1',
            "v":'V IY1',
            "w":'D AH1 . B AH0 L . Y UW0',
            "x":'EH1 K S',
            "y":'W AY1',
            "z":'Z IY1'
        }
        self.word2phone = load_word2phone(phonemes)

    def normalize(self, text):
        words: List[Word] = list()
        for word in text.lower():
            if word in self.word2phone:
                words.append(Word(content=word, phoneme=self.word2phone[word], rhythm=Rhythm.SHARP1, weight=999))
        return words


def load_word2phone(phonemes):
    word2phone = dict()
    for k, v in phonemes.items():
        phonemes = v.replace('w u', 'u').replace('y i', 'i').replace('w', 'u').replace('y', 'i').replace('oi', 'o i').replace('n g', 'ing')
        word2phone[k] = phonemes
    print(word2phone)
    return word2phone


def digit2chntext(text, alt_one=False, split_long=True):
    num_sys = NumberSystem()
    text = seq_num_to_chn(text, num_sys)
    if split_long:
        text = long_to_short(text)
    if alt_one == True:
        text = text.replace("一", "幺")

    return text


def digit_normalize(text, alt_one=False, split_long=True):
    pattern = re.compile(r"((\d+))")
    matchers = pattern.findall(text)
    if matchers:
        for matcher in matchers:
            target = matcher[0]
            target = digit2chntext(target, alt_one=False, split_long=True)
            text = text.replace(matcher[0], target, 1)
    return text


if __name__ == '__main__':
    print(digit_normalize('编号：31520181154418。'))
    print(digit2chntext('12345672234', alt_one=True))
