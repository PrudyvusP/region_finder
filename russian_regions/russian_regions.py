# https://regex101.com/r/jO3iI9/1
# https://regex101.com/r/FO68Xo/1
# https://regex101.com/r/wjUGj9/1

import re
from typing import List


class Region:
    _postcode_regex = re.compile(r'((?<![.:\d])\d{6}(?![:\d]))')

    _region_name_regex = re.compile(
        r'\b(?:северная осетия|марий эл|[а-яё]{2,}-?[а-яё]{2,})'
        r'(?= (?:автономн[аы][яй] о(?:бласть|круг)'
        r'|область|обл\.?'
        r'|(?:народная )*республика'
        r'|респ\.?'
        r'|край'
        r'|кр\.)\b)'
        r'|\b(?:москва|севастополь|санкт-петербург)\b'
        r'|(?:(?<=область )'
        r'|(?<=обл\. )'
        r'|(?<=\bобл )'
        r'|(?<=республика )'
        r'|(?<=\bресп\. )'
        r'|(?<=\bресп )'
        r'|(?<=край )'
        r'|(?<=\bкр\. ))'
        r'(?:северная осетия|марий эл|\b[а-яё]{2,}-?[а-яё]{2,})')

    _city_name_regex = re.compile(
        r'\b(?:г\.?|город) ?'
        r'('
        r'(?:'
        r'(?:'
        r'стар[аы][йя]'
        r'|нов[аы][йя]'
        r'|нижн[ия][йея]'
        r'|красный'
        r'|верхн[ия][йея]'
        r'|велики[ей]'
        r'|белая'
        r'|советская'
        r'|сергиев'
        r'|полярные'
        r'|петров'
        r'|павловский'
        r'|набережные'
        r'|минеральные'
        r'|мариинский'
        r'|малая'
        r'|лодейное'
        r'|западная'
        r'|дагестанские'
        r'|горячий'
        r'|гаврилов'
        r'|вятские'
        r'|вышний|'
        r'большой'
        r')'
        r' )*'
        r'\b[а-яё]+-?[а-яё]+-?[а-яё]+)'
    )
    _district_regex = re.compile(
        r'\b\w+-?\w+\b(?= \bрайон\b| \bр-о?н\b)'
    )

    _settlement_regex = re.compile(
        r'(?:(?<=\bр\.п\. )'
        r'|(?<=\bн\.п\. )'
        r'|(?<=\bп\. )'
        r'|(?<=\bс\. )'
        r'|(?<=\bпгт\. )'
        r'|(?<=\bпгт )'
        r'|(?<=\bсело )'
        r'|(?<=\bпоселок ))'
        r'(\b[а-яё]+-?[а-яё]+)'
    )

    def __init__(self, address):
        self.address = address.lower()

    def _find_postcodes(self) -> List[str]:
        """Возвращает список почтовых индексов
         - последовательности из 6 цифр."""

        return self._postcode_regex.findall(self.address)

    def _find_region_names(self) -> List[str]:
        """Возвращает список названий регионов."""

        return self._region_name_regex.findall(self.address)

    def _find_city_names(self) -> List[str]:
        """Возвращает список названий городов
        по характерным признакам перед их названиями
        (буква г с точкой или без)."""

        return self._city_name_regex.findall(self.address)

    def _find_district_names(self) -> List[str]:
        """Возвращает список названий районов."""

        return self._district_regex.findall(self.address)

    def _find_settlement_names(self) -> List[str]:
        """Возвращает список названий поселков
         городского типа, поселков и сел."""

        return self._settlement_regex.findall(self.address)

    def define_region(self):
        """Возвращает список названий регионов."""

        ...


"""
if __name__ == '__main__':
    with open('input_file.txt', 'r') as f:
        addresses = [strq.strip('\n') for strq in f.readlines()]
        for address in addresses:
            r = Region(address)
            result = r._find_region_names()
            print(r._find_region_names())
        ##print(data)
"""
