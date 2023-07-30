# https://regex101.com/r/jO3iI9/1
import re
from typing import List, Set


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

    def __init__(self, address):
        self.address = address.lower()

    def _find_postcodes(self) -> List[str]:
        """Возвращает список почтовых индексов
         - последовательности из 6 цифр."""

        return self._postcode_regex.findall(self.address)

    def _find_region_names(self) -> List[str]:
        """Возвращает список названий регионов."""

        return self._region_name_regex.findall(self.address)

    def _get_unique_region_names(self) -> Set[str]:
        """Возвращает множество уникальных названий регионов."""

        return set(self._find_region_names())

    def _find_city_and_settlement_names(self) -> List[str]:
        """Возвращает список названий городов и сел
        по характерным признакам перед их названиями (г., с., пгт. и т.д.)."""

        ...

    def _find_district_names(self) -> List[str]:
        """Возвращает название районов."""

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
