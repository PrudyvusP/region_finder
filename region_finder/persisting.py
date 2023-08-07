import argparse
import json
from typing import List, Tuple, Dict

from dbfread import DBF

from models import Region, Alias, Address
from session import session


def cast_region_name_to_constitute(region_name: str) -> str:
    """Преобразует название региона
     в соответствии со ст. 65 Конституцией РФ."""

    region = region_name.lower()
    if region == 'кемеровская область':
        return 'Кемеровская область - Кузбасс'
    elif region in ('южная осетия', 'казахстан', 'германия'):
        return 'Иные территории, включая город и космодром Байконур'
    elif region == 'чувашия республика':
        return 'Чувашская Республика - Чувашия'
    elif region == 'ханты-мансийский-югра автономный округ':
        return 'Ханты-Мансийский автономный округ - Югра'
    elif region == 'ямало-ненецкий автономный округ':
        return 'Ямало-Ненецкий автономный округ'
    if 'область' in region or 'край' in region:
        return region.capitalize()
    if 'автономный' in region and 'округ' in region:
        return region.capitalize()
    region = region.title()
    if 'Республика' in region:
        if region.split()[0].endswith('кая'):
            return region
        else:
            return f'Республика {region.split("Республика")[0].rstrip()}'
    return region


def create_postcodes_from_dbf(postcodes: DBF,
                              regions: Dict) -> List[Address]:
    """Возвращает список объектов типа Address
    из последовательности postcodes."""

    postcodes_for_db = []
    for postcode in postcodes:
        locality = postcode.get('CITY').lower()
        area = postcode.get('AREA').replace(' РАЙОН', '').lower()
        postcode_region = postcode.get('REGION') or postcode.get('AUTONOM')
        region_id = regions[cast_region_name_to_constitute(postcode_region)]
        postcodes_for_db.append(
            Address(region_id=region_id, postcode=postcode.get('INDEX'),
                    area=area, locality=locality)
        )
    return postcodes_for_db


def parse_arguments() -> DBF:
    """Возвращает объект типа DBF по переданному как параметр имени."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        help='путь до файла .dbf, содержащего базу почтовых индексов')
    args = parser.parse_args()
    if not args.filename.endswith('.dbf'):
        raise TypeError('необходимо передать путь до файла с расширением .dbf')

    return DBF(args.filename)


def create_region_and_alias_objects(
        data: List[Dict]
) -> Tuple[List[Region], List[Alias]]:
    """Создает списки объектов типа Region и Alias
    из переданного списка словарей data."""

    regions_for_db, aliases_for_db = [], []

    for d in data:
        region_id = d['region_id']
        new_region = Region(region_id=region_id, name=d['name'])
        regions_for_db.append(new_region)
        for alias in d['aliases']:
            new_alias = Alias(region_id=region_id, name=alias)
            aliases_for_db.append(new_alias)

    return regions_for_db, aliases_for_db


def main_logic() -> None:
    """Заполняет БД регионами РФ и их алиасами, а также
    почтовыми индексами РФ."""

    postcodes = parse_arguments()

    with open('regions.json', 'r') as f:
        regions_and_aliases = json.load(f)

    new_regions, new_aliases = create_region_and_alias_objects(regions_and_aliases)
    region_names_ids = {region.name: region.region_id for region in new_regions}
    new_postcodes = create_postcodes_from_dbf(postcodes, region_names_ids)

    with session:
        for item in [new_regions, new_aliases, new_postcodes]:
            session.bulk_save_objects(item)
        session.commit()


if __name__ == '__main__':
    main_logic()
