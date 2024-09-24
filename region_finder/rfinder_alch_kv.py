import re
from typing import Dict

from region_finder_ru.region_finder_ru import RegionFinder
from sqlalchemy import distinct, func, select

from region_finder.models import Address, Alias, Region, Town

word_splitter_regex = re.compile(r'[.;,\n\t: ]')


class RegionDataGetter:

    def __init__(self, session):
        self.session = session

    def get_regions(self) -> Dict[int, str]:
        """
            SELECT region_id, name
            FROM regions;
        """
        regions_q = (
            self
            .session
            .execute(
                select(Region.name, Region.region_id))
            .all()
        )
        return {region_id: name for name, region_id in regions_q}

    def get_aliases(self) -> Dict[str, int]:
        """
            SELECT name, region_id
            FROM aliases;
        """
        aliases_q = (
            self
            .session
            .execute(
                select(Alias.name,
                       Alias.region_id))
            .all()
        )
        return {name: region_id for name, region_id in aliases_q}

    def get_unique_districts(self) -> Dict[str, int]:
        """
            SELECT DISTINCT area, region_id
            FROM addresses
            WHERE addresses.area IN
            (SELECT addresses.area
            FROM addresses
            GROUP by addresses.area
            HAVING COUNT(DISTINCT addresses.region_id) = 1);
        """
        districts_subq = (
            select(Address.area)
            .group_by(Address.area)
            .having(func.count(distinct(Address.region_id)) == 1)
        )

        districts_q = (
            self
            .session
            .execute(
                select(distinct(Address.area), Address.region_id)
                .where(Address.area.in_(districts_subq)))
            .all()
        )
        return {name: region_id for name, region_id in districts_q}

    def get_unique_towns(self) -> Dict[str, int]:
        """
            SELECT DISTINCT name, region_id
            FROM towns
            WHERE towns.name IN
            (SELECT towns.name
            FROM towns
            GROUP by towns.name
            HAVING COUNT(DISTINCT towns.region_id) = 1);
        """
        towns_subq = (
            select(Town.name)
            .group_by(Town.name)
            .having(func.count(distinct(Town.region_id)) == 1)
        )

        towns_q = (
            self
            .session
            .execute(
                select(distinct(Town.name), Town.region_id)
                .where(Town.name.in_(towns_subq)))
            .all()
        )
        return {name: region_id for name, region_id in towns_q}

    def get_unique_localities(self) -> Dict[str, int]:
        """
            SELECT DISTINCT locality, region_id FROM addresses
            WHERE addresses.locality IN
            (SELECT addresses.locality
            FROM addresses
            GROUP by addresses.locality
            HAVING COUNT(DISTINCT addresses.region_id) = 1);
        """
        localities_subq = (
            select(Address.locality)
            .group_by(Address.locality)
            .having(func.count(distinct(Address.region_id)) == 1)
        )

        localities_q = (
            self
            .session
            .execute(
                select(distinct(Address.locality), Address.region_id)
                .where(Address.locality.in_(localities_subq)))
            .all()
        )
        return {name: region_id for name, region_id in localities_q}

    def get_ps_prefixes(self) -> Dict[str, int]:
        """
            SELECT SUBSTRING(postcode, 1, 3) AS ps_prefix, region_id
            FROM addresses;
            GROUP BY ps_prefix;
        """
        postcodes_q = (
            self
            .session
            .execute(
                select(func.substr(Address.postcode, 1, 3).label('ps_prefix'),
                       Address.region_id)
                .group_by('ps_prefix'))
            .all()
        )
        return {ps_prefix: region_id for ps_prefix, region_id in postcodes_q}

    def get_all_data(self) -> Dict[str, Dict]:
        """Возвращает все эталонные гео данные."""

        return {
            "aliases": self.get_aliases(),
            "districts": self.get_unique_districts(),
            "localities": self.get_unique_localities(),
            "regions": self.get_regions(),
            "towns": self.get_unique_towns(),
            "ps_prefixes": self.get_ps_prefixes()
        }


class RegionFinderWithKV(RegionFinder):

    def split_address_by_symbols(self):
        return word_splitter_regex.split(self.address)

    @staticmethod
    def define_regions_by_param(seq, regex_func) -> set:
        results = set()
        found_params = regex_func()
        if found_params:
            for found_param in found_params:
                if seq.get(found_param):
                    results.add(seq[found_param])
        return results

    def define_regions(self, **kwargs):

        ps_prefixes = kwargs.get('ps_prefixes')
        aliases = kwargs.get('aliases')

        regions_names = self.define_regions_by_param(
            seq=aliases, regex_func=self._find_region_names)
        regions_postcodes_first_3 = self.define_regions_by_param(
            seq=ps_prefixes, regex_func=self._find_first_3_postcodes)
        regions_names.update(regions_postcodes_first_3)
        if regions_names:
            return regions_names

        towns = kwargs.get('towns')
        regions_towns = self.define_regions_by_param(
            seq=towns, regex_func=self._find_city_names)
        if regions_towns:
            return regions_towns

        districts = kwargs.get('districts')
        regions_districts = self.define_regions_by_param(
            seq=districts, regex_func=self._find_district_names)
        if regions_districts:
            return regions_districts

        settlements = kwargs.get('settlements')
        regions_settlements = self.define_regions_by_param(
            seq=settlements, regex_func=self._find_settlement_names)
        if regions_settlements:
            return regions_settlements

        return {}
