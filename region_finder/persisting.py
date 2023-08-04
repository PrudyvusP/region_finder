from typing import List

from dbfread import DBF

from models import Region, Alias, Address
from session import session

regions = [
    {'region_id': 1, 'name': 'Республика Адыгея', 'aliases': ['адыгея']},
    {'region_id': 2, 'name': 'Республика Башкортостан', 'aliases': ['башкортостан']},
    {'region_id': 3, 'name': 'Республика Бурятия', 'aliases': ['бурятия']},
    {'region_id': 4, 'name': 'Республика Алтай', 'aliases': ['алтай']},
    {'region_id': 5, 'name': 'Республика Дагестан', 'aliases': ['дагестан']},
    {'region_id': 6, 'name': 'Республика Ингушетия', 'aliases': ['ингушетия']},
    {'region_id': 7, 'name': 'Кабардино-Балкарская Республика',
     'aliases': ['кабардино', 'балкарская', 'кабардино-балкарская']},
    {'region_id': 8, 'name': 'Республика Калмыкия', 'aliases': ['калмыкия']},
    {'region_id': 9, 'name': 'Карачаево-Черкесская Республика',
     'aliases': ['карачаево', 'черкесская', 'карачаево-черкесская']},
    {'region_id': 10, 'name': 'Республика Карелия', 'aliases': ['карелия']},
    {'region_id': 11, 'name': 'Республика Коми', 'aliases': ['коми']},
    {'region_id': 12, 'name': 'Республика Марий Эл', 'aliases': ['марий эл', 'марий']},
    {'region_id': 13, 'name': 'Республика Мордовия', 'aliases': ['мордовия']},
    {'region_id': 14, 'name': 'Республика Саха (Якутия)', 'aliases': ['саха', 'якутия']},
    {'region_id': 15, 'name': 'Республика Северная Осетия - Алания', 'aliases': ['северная осетия', 'алания']},
    {'region_id': 16, 'name': 'Республика Татарстан', 'aliases': ['татарстан']},
    {'region_id': 17, 'name': 'Республика Тыва', 'aliases': ['тыва']},
    {'region_id': 18, 'name': 'Удмуртская Республика', 'aliases': ['удмуртская', 'удмуртия']},
    {'region_id': 19, 'name': 'Республика Хакасия', 'aliases': ['хакасия']},
    {'region_id': 20, 'name': 'Чеченская Республика', 'aliases': ['чеченская']},
    {'region_id': 21, 'name': 'Чувашская Республика - Чувашия', 'aliases': ['чувашская', 'чувашия']},
    {'region_id': 22, 'name': 'Алтайский край', 'aliases': ['алтайский']},
    {'region_id': 23, 'name': 'Краснодарский край', 'aliases': ['краснодарский']},
    {'region_id': 24, 'name': 'Красноярский край', 'aliases': ['красноярский']},
    {'region_id': 25, 'name': 'Приморский край', 'aliases': ['приморский']},
    {'region_id': 26, 'name': 'Ставропольский край', 'aliases': ['ставропольский']},
    {'region_id': 27, 'name': 'Хабаровский край', 'aliases': ['хабаровский']},
    {'region_id': 28, 'name': 'Амурская область', 'aliases': ['амурская']},
    {'region_id': 29, 'name': 'Архангельская область', 'aliases': ['архангельская']},
    {'region_id': 30, 'name': 'Астраханская область', 'aliases': ['астраханская']},
    {'region_id': 31, 'name': 'Белгородская область', 'aliases': ['белгородская']},
    {'region_id': 32, 'name': 'Брянская область', 'aliases': ['брянская']},
    {'region_id': 33, 'name': 'Владимирская область', 'aliases': ['владимирская']},
    {'region_id': 34, 'name': 'Волгоградская область', 'aliases': ['волгоградская']},
    {'region_id': 35, 'name': 'Вологодская область', 'aliases': ['вологодская']},
    {'region_id': 36, 'name': 'Воронежская область', 'aliases': ['воронежская']},
    {'region_id': 37, 'name': 'Ивановская область', 'aliases': ['ивановская']},
    {'region_id': 38, 'name': 'Иркутская область', 'aliases': ['иркутская']},
    {'region_id': 39, 'name': 'Калининградская область', 'aliases': ['калининградская']},
    {'region_id': 40, 'name': 'Калужская область', 'aliases': ['калужская']},
    {'region_id': 41, 'name': 'Камчатский край', 'aliases': ['камчатский']},
    {'region_id': 42, 'name': 'Кемеровская область - Кузбасс', 'aliases': ['кемеровская', 'кузбасс']},
    {'region_id': 43, 'name': 'Кировская область', 'aliases': ['кировская']},
    {'region_id': 44, 'name': 'Костромская область', 'aliases': ['костромская']},
    {'region_id': 45, 'name': 'Курганская область', 'aliases': ['курганская']},
    {'region_id': 46, 'name': 'Курская область', 'aliases': ['курская']},
    {'region_id': 47, 'name': 'Ленинградская область', 'aliases': ['ленинградская']},
    {'region_id': 48, 'name': 'Липецкая область', 'aliases': ['липецкая']},
    {'region_id': 49, 'name': 'Магаданская область', 'aliases': ['магаданская']},
    {'region_id': 50, 'name': 'Московская область', 'aliases': ['московская']},
    {'region_id': 51, 'name': 'Мурманская область', 'aliases': ['мурманская']},
    {'region_id': 52, 'name': 'Нижегородская область', 'aliases': ['нижегородская']},
    {'region_id': 53, 'name': 'Новгородская область', 'aliases': ['новгородская']},
    {'region_id': 54, 'name': 'Новосибирская область', 'aliases': ['новосибирская']},
    {'region_id': 55, 'name': 'Омская область', 'aliases': ['омская']},
    {'region_id': 56, 'name': 'Оренбургская область', 'aliases': ['оренбургская']},
    {'region_id': 57, 'name': 'Орловская область', 'aliases': ['орловская']},
    {'region_id': 58, 'name': 'Пензенская область', 'aliases': ['пензенская']},
    {'region_id': 59, 'name': 'Пермский край', 'aliases': ['пермский']},
    {'region_id': 60, 'name': 'Псковская область', 'aliases': ['псковская']},
    {'region_id': 61, 'name': 'Ростовская область', 'aliases': ['ростовская']},
    {'region_id': 62, 'name': 'Рязанская область', 'aliases': ['рязанская']},
    {'region_id': 63, 'name': 'Самарская область', 'aliases': ['самарская']},
    {'region_id': 64, 'name': 'Саратовская область', 'aliases': ['саратовская']},
    {'region_id': 65, 'name': 'Сахалинская область', 'aliases': ['сахалинская']},
    {'region_id': 66, 'name': 'Свердловская область', 'aliases': ['свердловская']},
    {'region_id': 67, 'name': 'Смоленская область', 'aliases': ['смоленская']},
    {'region_id': 68, 'name': 'Тамбовская область', 'aliases': ['тамбовская']},
    {'region_id': 69, 'name': 'Тверская область', 'aliases': ['тверская']},
    {'region_id': 70, 'name': 'Томская область', 'aliases': ['томская']},
    {'region_id': 71, 'name': 'Тульская область', 'aliases': ['тульская']},
    {'region_id': 72, 'name': 'Тюменская область', 'aliases': ['тюменская']},
    {'region_id': 73, 'name': 'Ульяновская область', 'aliases': ['ульяновская']},
    {'region_id': 74, 'name': 'Челябинская область', 'aliases': ['челябинская']},
    {'region_id': 75, 'name': 'Забайкальский край', 'aliases': ['забайкальский']},
    {'region_id': 76, 'name': 'Ярославская область', 'aliases': ['ярославская']},
    {'region_id': 77, 'name': 'Москва', 'aliases': ['москва']},
    {'region_id': 78, 'name': 'Санкт-Петербург', 'aliases': ['санкт-петербург']},
    {'region_id': 79, 'name': 'Еврейская автономная область', 'aliases': ['еврейская']},
    {'region_id': 83, 'name': 'Ненецкий автономный округ', 'aliases': ['ненецкий']},
    {'region_id': 86, 'name': 'Ханты-Мансийский автономный округ - Югра', 'aliases': ['ханты-мансийский']},
    {'region_id': 87, 'name': 'Чукотский автономный округ', 'aliases': ['чукотский']},
    {'region_id': 89, 'name': 'Ямало-Ненецкий автономный округ', 'aliases': ['ямало-ненецкий']},
    {'region_id': 91, 'name': 'Республика Крым', 'aliases': ['крым']},
    {'region_id': 92, 'name': 'Севастополь', 'aliases': ['севастополь']},
    {'region_id': 99, 'name': 'Иные территории, включая город и космодром Байконур', 'aliases': []},
]


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


def read_from_dbf(filename: str) -> DBF:
    """Возвращает объект типа DBF по переданному имени."""

    if not filename.endswith('.dbf'):
        raise TypeError('необходимо грузить .dbf-файлы')

    return DBF(filename)


def get_postcodes_from_dbf(postcodes: DBF,
                           regions: dict) -> List[Address]:
    """Возвращает список объектов типа Address
    из последовательности postcodes."""

    new_postcodes = []
    for postcode in postcodes:
        locality = postcode.get('CITY').lower()
        area = postcode.get('AREA').replace(' РАЙОН', '').lower()
        postcode_region = postcode.get('REGION') or postcode.get('AUTONOM')
        region_id = regions[cast_region_name_to_constitute(postcode_region)]
        new_postcodes.append(
            Address(region_id=region_id, postcode=postcode.get('INDEX'),
                    area=area, locality=locality)
        )
    return new_postcodes


if __name__ == '__main__':
    new_regions, new_aliases = [], []

    for region in regions:
        region_id = region['region_id']
        new_region = Region(region_id=region_id, name=region['name'])
        new_regions.append(new_region)
        for alias in region['aliases']:
            new_alias = Alias(region_id=region_id, name=alias)
            new_aliases.append(new_alias)

    postcodes = read_from_dbf('PIndx09.dbf')
    region_names_ids = {region.name: region.region_id for region in new_regions}
    new_postcodes = get_postcodes_from_dbf(postcodes, region_names_ids)

    with session:
        for item in [new_regions, new_aliases, new_postcodes]:
            session.bulk_save_objects(item)
        session.commit()
