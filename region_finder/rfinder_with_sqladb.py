from typing import List, Set

from region_finder_ru.region_finder_ru import RegionFinder
from sqlalchemy import func, select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .models import Address, Alias, Region

UNIQUE_REGION_CONST = 1


class RegionFinderWithSQLADB(RegionFinder):

    def __init__(self, address, session):
        """Конструктор класса."""

        super().__init__(address)
        self.session = session

    def define_regions(self) -> Set["Region"]:
        """Переопределяет логику для поиска
        сущностей из справочной БД."""

        def get_aliases_from_db(aliases: List[str]) -> List["Region"]:
            """Возвращает список объектов типа Region,
            чьи алиасы в списке aliases."""

            alias_query = (
                select(Region.name)
                .join(Alias, Region.aliases)
                .where(Alias.name.in_(aliases))
            )
            return self.session.scalars(alias_query).all()

        def get_postcodes_from_db(postcodes: List[str]) -> List["Region"]:
            """Возвращает список объектов типа Region,
            чьи почтовые индексы в списке postcodes."""

            postcode_query = (
                select(Region.name)
                .join(Address, Region.addresses)
                .where(
                    Address.postcode.in_(postcodes)
                )
            )
            return self.session.scalars(postcode_query).all()

        def get_instances_from_db(
                sequence: List[str],
                model_column: InstrumentedAttribute) -> Set["Region"]:
            """Возвращает множество объектов типа Region,
            проверяя каждый элемент последовательности sequence на случай,
            его существования только в составе одного региона РФ."""

            regions = set()
            for item in sequence:
                item_check_query = (
                    select(func.count(Region.region_id.distinct()))
                    .join(Address, Region.addresses)
                    .where(model_column == item)
                )

                if (self.session.scalar(item_check_query)
                        == UNIQUE_REGION_CONST):
                    item_from_city_query = (
                        select(Region.name)
                        .join(Address, Region.addresses)
                        .where(model_column == item)
                    )
                    regions.add(
                        self.session.scalars(item_from_city_query).first()
                    )
            return regions

        results = set()

        aliases = self._find_region_names()
        for result in get_aliases_from_db(aliases):
            results.add(result)

        postcodes = self._find_postcodes()
        for result in get_postcodes_from_db(postcodes):
            results.add(result)

        if results:
            return results

        cities = self._find_city_names()
        regions_from_cities = get_instances_from_db(cities,
                                                    Address.locality)
        if regions_from_cities:
            return regions_from_cities

        districts = self._find_district_names()
        regions_from_districts = get_instances_from_db(districts,
                                                       Address.area)
        if regions_from_districts:
            return regions_from_districts

        settlements = self._find_settlement_names()
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
                    .join(Address, Region.addresses)
                    .where(Address.locality == city)
                    .group_by(Region.region_id)
                    .order_by(func.count(Address.postcode).desc())
                    .limit(1)
                )
                region_max_id = self.session.scalar(region_max_id_query)
                if region_max_id:
                    region_id_query = (
                        select(Region.name)
                        .where(Region.region_id == region_max_id)
                    )
                    result = self.session.scalars(region_id_query).first()
                    if result:
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
                    .join(Address, Region.addresses)
                    .where(Address.postcode.like(search_pattern))
                )
                result = self.session.scalars(alias_query).first()
                if result:
                    results.add(result)

        return results
