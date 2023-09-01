import pytest

from region_finder.rfinder_with_sqladb import RegionFinderWithSQLADB


class TestRegionFinderWithSQLADB:
    """Класс TestRegionFinderWithSQLADB используется для поиска
     тестирования правильности бизнес-логики определения региона
     в адресной строке с использованием СУБД.

    Методы
    -------
    test_define_by_postcode():
        Проверяет определение регионов по почтовым индексам.
    test_define_by_region_name():
        Проверяет определение регионов по названиям регионов.
    test_define_by_unique_settlement():
        Проверяет определение регионов по уникальным названиям
        поселков или сел.
    test_define_by_unique_district_name():
        Проверяет определение регионов по уникальным
        названиям районов.
    test_define_by_city_double_name():
        Проверяет определение регионов у городов, названия которых
        состоят из двух слов.
    test_define_by_postcode_prefix():
        Проверяет определение регионов по почтовым индексам,
        которые отсутствуют в БД.
    test_define_no_region():
        Проверяет отсутствие регионов в некорректных адресных строках.
    test_empty_address():
        Проверяет обработку исключения пустого адреса.
    test_postcode_regions_first():
        Проверяет определение регионов только по почтовым индексам
        и названиям регионов.
    test_define_cities_only():
        Проверяет определение регионов по городам, в случае
        если не удалось вернуть результат по почтовым индексам
        и названиям регионов.
    test_define_districts_only():
        Проверяет определение регионов по городам, в случае
        если не удалось вернуть результат по почтовым индексам
        и названиям регионов.
    test_define_by_not_unique_localities():
        Проверяет определение регионов по неуникальным
        названиям городов.
    """

    def test_define_by_postcode(self, db_session_with_data):
        """Корректное определение по почтовому индексу."""

        address = '125039 г Москва, ул Сергея Макеева, дом 2 стр. 1 '
        r = RegionFinderWithSQLADB(address,
                                   db_session_with_data)
        assert {'Москва'} == r.define_regions()

    def test_define_by_region_name(self, db_session_with_data):
        """Корректное определение по названию региона."""

        address = ('ПРИМОРСКИЙ край г. Владивосток, Москва,'
                   'область Ленинградская')
        r = RegionFinderWithSQLADB(address,
                                   db_session_with_data)
        assert {'Приморский край',
                'Москва',
                'Ленинградская область'} == r.define_regions()

    def test_define_by_unique_settlement(self, db_session_with_data):
        """Корректное определение по уникальному названию посёлка."""

        address = 'п. берикуль советская ул. 11'
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Кемеровская область - Кузбасс'} == r.define_regions()

    def test_define_by_unique_district_name(self, db_session_with_data):
        """Корректное определение по уникальному названию района."""

        address = 'ЯНАО Ямальский район лесное месторождение'
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Ямало-Ненецкий автономный округ'} == r.define_regions()

    def test_define_by_city_double_name(self, db_session_with_data):
        """Корректное определение по названию города из двух слов."""

        address = 'г. Верхний Уфалей озеро приколов'
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Челябинская область'} == r.define_regions()

    def test_define_by_postcode_prefix(self, db_session_with_data):
        """Корректное определение по первым трем символам почтового индекса."""

        address = '456806 Уфалей (Верхний) ул. Уфалейская'
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Челябинская область'} == r.define_regions()

    def test_define_no_region(self, db_session_with_data):
        """Плохой адрес = нет регионов."""

        address = ('12552 Мсква улица Омская дом 15 республика'
                   'Тотарстан 57.584724, 34.547930 город город'
                   'РБ')
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert not r.define_regions()

    def test_empty_address(self, db_session_with_data):
        """Пустой адрес вызывает ошибку ValueError."""

        with pytest.raises(ValueError):
            RegionFinderWithSQLADB('', db_session_with_data)

    def test_postcode_regions_first(self, db_session_with_data):
        """Если в строке найден регион по почтовому индексу
        или названию региона, то остальные случаи не обрабатываются."""

        address = ('125039 Ленинградское шоссе 11\n'
                   '692910 г. Находка, ул. Приморская 77\n'
                   'Ивановская область Иваново ул. Лесная 1\n'
                   'г. Саяногорск, п. Урвань, п. Берикуль')

        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Москва',
                'Приморский край',
                'Ивановская область'} == r.define_regions()

    def test_define_cities_only(self, db_session_with_data):
        """Если поиск по почтовым индексам и названиям регионов
        не дал результатов, то обрабатываются только города."""

        address = ('Ленинградское шоссе 11\n'
                   'г. Находка, ул. Приморская 77\n'
                   'Иваново ул. Лесная 1\n'
                   'г. Саяногорск, п. Урвань, п. Берикуль')
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Приморский край',
                'Республика Хакасия'} == r.define_regions()

    def test_define_districts_only(self, db_session_with_data):
        """Если поиск по почтовым индексам, названиям регионов
        и названиям городов не дал результатов, то обрабатываются
        только районы."""

        address = ('Ленинградское шоссе 11\n'
                   'Находка, ул. Приморская 77\n'
                   'Иваново ул. Лесная 1\n'
                   'Саяногорск, п. Урвань, п. Берикуль,'
                   'ямальский район ЯНАО')
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Ямало-Ненецкий автономный округ'} == r.define_regions()

    def test_define_by_not_unique_localities(self, db_session_with_data):
        """Если поиск по почтовым индексам, названиям регионов,
        уникальным названиям городов и названиям районов не дал
        результатов, то ищутся неуникальные города и выбирается
        тот, у которого почтовых отделений больше."""

        address = 'г. Иваново ул. Тестов 15'
        r = RegionFinderWithSQLADB(address, db_session_with_data)
        assert {'Ивановская область'} == r.define_regions()
