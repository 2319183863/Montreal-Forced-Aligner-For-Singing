from typing import Optional
from LeTTS.common.enum.text_content import TextContent
from LeTTS.text.chinese.normalizer.normalizer import Normalizer
from LeTTS.text.chinese.normalizer.car_number import CarNumber
from LeTTS.text.chinese.normalizer.date import Date
from LeTTS.text.chinese.normalizer.english import English
from LeTTS.text.chinese.normalizer.measure import Measure
from LeTTS.text.chinese.normalizer.money import Money
from LeTTS.text.chinese.normalizer.number import Number, Cardinal
from LeTTS.text.chinese.normalizer.digit import Digits
from LeTTS.text.chinese.normalizer.special import Special
from LeTTS.text.chinese.normalizer.symbol import Symbol
from LeTTS.text.chinese.normalizer.telephone import TelePhone
from LeTTS.text.chinese.normalizer.characters import Characters


class NormalizerFactory:
    @staticmethod
    def create_normalizer(text_content: TextContent) -> Optional[Normalizer]:
        normalizer = None
        if text_content == TextContent.CAR_NUMBER.value:
            normalizer = CarNumber()
        elif text_content == TextContent.DATE.value:
            normalizer = Date()
        elif text_content == TextContent.ENGLISH.value:
            normalizer = English()
        elif text_content == TextContent.MEASURE.value:
            normalizer = Measure()
        elif text_content == TextContent.MONEY.value:
            normalizer = Money()
        elif text_content == TextContent.NUMBER.value:
            normalizer = Number(True)
        elif text_content == TextContent.SPECIAL.value:
            normalizer = Special()
        elif text_content == TextContent.SYMBOL.value:
            normalizer = Symbol()
        elif text_content == TextContent.TELEPHONE.value:
            normalizer = TelePhone()
        elif text_content == TextContent.CARDINAL.value:
            normalizer = Cardinal()
        elif text_content == TextContent.DIGITS.value:
            normalizer = Digits()
        elif text_content == TextContent.CHARACTERS.value:
            normalizer = Characters()
        return normalizer
