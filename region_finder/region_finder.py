import os
import sys
from typing import List, Set

from sqlalchemy import select, func
from sqlalchemy.orm.attributes import InstrumentedAttribute

from models import Region, Alias, Address
from session import session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from russian_regions.russian_regions import RegionFinder

UNIQUE_REGION_CONST = 1


class RegionFinderWithSQLADB(RegionFinder):

    def define_regions(self) -> Set[Region]:
        """Переопределяет логику для поиска
        сущностей из справочной БД."""

        def get_aliases_from_db(aliases: List[str]) -> List[Region]:
            """Возвращает список объектов типа Region,
            чьи алиасы в списке aliases."""

            alias_query = (
                select(Region.name)
                .join(Alias, Region.aliases)
                .where(Alias.name.in_(aliases))
            )
            return session.scalars(alias_query).all()

        def get_postcodes_from_db(postcodes: List[str]) -> List[Region]:
            """Возвращает список объектов типа Region,
            чьи почтовые индексы в списке postcodes."""

            postcode_query = (
                select(Region.name)
                .join(Address, Address.region_id == Region.region_id)
                .where(
                    Address.postcode.in_(postcodes)
                )
            )
            return session.scalars(postcode_query).all()

        def get_instances_from_db(
                sequence: List[str],
                model_column: InstrumentedAttribute) -> Set[Region]:
            """Возвращает множество объектов типа Region,
            проверяя каждый элемент последовательности sequence на случай,
            его существования только в составе одного региона РФ."""

            regions = set()
            for item in sequence:
                item_check_query = (
                    select(func.count(Region.region_id.distinct()))
                    .join(Address, Address.region_id == Region.region_id)
                    .where(model_column == item)
                )

                if session.scalar(item_check_query) == UNIQUE_REGION_CONST:
                    item_from_city_query = (
                        select(Region.name)
                        .join(Address, Address.region_id == Region.region_id)
                        .where(model_column == item)
                    )
                    regions.add(session.scalars(item_from_city_query).first())
            return regions

        results = set()

        aliases = self._find_region_names()
        if aliases:
            for result in get_aliases_from_db(aliases):
                results.add(result)

        postcodes = self._find_postcodes()
        if postcodes:
            for result in get_postcodes_from_db(postcodes):
                if result not in results:
                    results.add(result)

        if results:
            return results

        cities = self._find_city_names()
        if cities:
            regions_from_cities = get_instances_from_db(cities,
                                                        Address.locality)
            if regions_from_cities:
                return regions_from_cities

        districts = self._find_district_names()
        if districts:
            regions_from_districts = get_instances_from_db(districts,
                                                           Address.area)
            if regions_from_districts:
                return regions_from_districts

        settlements = self._find_settlement_names()
        if settlements:
            settlements_from_cities = get_instances_from_db(settlements,
                                                            Address.locality)
            if settlements_from_cities:
                return settlements_from_cities

        """
        Ищем города вероятностным подходом типа Калуга, Самара,
        Брянск, Кострома, Киров, Мичуринск, Сургут, Иваново,
        Владимир, Кропоткин, Горячий Ключ, Белореченск, Подольск,
        Находка, Ревда, Курск, Грозный,
        Благовещенск, Курган, Советский, Чехов, Зеленогорск
        """

        if cities:
            for city in set(cities):
                region_max_id_query = (
                    select(Region.region_id)
                    .join(Address, Address.region_id == Region.region_id)
                    .where(Address.locality == city)
                    .group_by(Region.region_id)
                    .order_by(func.count(Address.postcode).desc())
                    .limit(1)
                )
                region_max_id = session.scalar(region_max_id_query)
                if region_max_id:
                    region_id_query = (
                        select(Region.name)
                        .where(Region.region_id == region_max_id)
                    )
                    result = session.scalars(region_id_query).first()
                    if result and result not in results:
                        results.add(result)

        if results:
            return results

        """
        Обрабатываем ситуации, если почтовый индекс отсутствует в БД.
        """

        if postcodes:
            for postcode in postcodes:
                search_pattern = postcode[0:3] + '%'
                alias_query = (
                    select(Region.name)
                    .join(Address, Address.region_id == Region.region_id)
                    .where(Address.postcode.like(search_pattern))
                )
                result = session.scalars(alias_query).first()
                if result and result not in results:
                    results.add(result)

        return results


if __name__ == '__main__':
    with open('input_file.txt', 'r') as f:
        addresses = [strq.strip('\n') for strq in f.readlines()]
        for address in addresses:
            r = RegionFinderWithSQLADB(address)
            print(r.define_regions())
            print(r._find_region_names())
