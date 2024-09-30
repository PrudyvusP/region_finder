from region_finder.rfinder_alch_kv import RegionFinderWithKV, RegionDataGetter


class TestRegionDataGetter:
    """Класс TestRegionDataGetter используется для
    тестирования правильности отдачи подготовительных данных,
    необходимых для поиска регионов.

    Методы
    -------
    test_get_regions_ok():
        Проверяет корректность словаря с регионами.
    test_get_aliases_ok():
        Проверяет корректность словаря с алиасами регионов.
    test_get_unique_districts_ok():
        Проверяет корректность словаря с уникальными районами.
    test_get_unique_towns_ok():
        Проверяет корректность словаря с уникальными городами.
    test_get_unique_localities_ok():
        Проверяет корректность словаря с уникальными населенными пунктами.
    test_get_ps_prefixes():
        Проверяет корректность словаря с префиксами почтовых индексов.
    test_get_all_data():
        Проверяет корректность словаря с результатами всех методов.
    """

    REGION_IDS = [47, 42, 25, 77, 19, 7, 89, 37, 60, 74, 39, 43]

    ALIASES = [
        'ленинградская', 'кемеровская', 'кузбасс',
        'приморский', 'москва', 'хакасия',
        'кабардино-балкарская', 'ямало-ненецкий', 'ивановская',
        'псковская', 'челябинская', 'калининградская',
        'кировская']

    DICT_KEYS = ['aliases', 'districts', 'localities', 'regions',
                 'towns', 'ps_prefixes']

    PS_PREFIXES = ['125', '153', '182', '188', '361', '456',
                   '457', '629', '652', '655', '692']

    UNIQUE_DISTRICTS = ['выборгский', 'урванский', 'ямальский', 'ижморский',
                        'великолукский']

    UNIQUE_TOWNS = ['губкинский', 'фурманов', 'шуя']

    UNIQUE_LOCALITIES = ['находка', 'поляны', 'урвань',
                         'яр-сале', 'саяногорск', 'берикуль',
                         'верхний уфалей', 'подовинное', 'покровка']

    def test_get_regions_ok(self, db_session_full):
        """Корректный словарь с регионами."""
        r = RegionDataGetter(db_session_full)
        results = r.get_regions()
        assert len(results) == len(
            self.REGION_IDS), 'Кол-во регионов не совпадает'
        for reg_id in self.REGION_IDS:
            assert reg_id in results
        assert 50 not in results
        assert results[19] == 'Республика Хакасия'

    def test_get_aliases_ok(self, db_session_full):
        """Корректный словарь с алиасами регионов."""
        r = RegionDataGetter(db_session_full)
        results = r.get_aliases()
        assert len(results) == len(
            self.ALIASES), 'Кол-во алиасов регионов не совпадает'
        for alias in self.ALIASES:
            assert alias in results
        assert 'московская' not in results
        assert results['хакасия'] == 19

    def test_get_unique_districts_ok(self, db_session_full):
        """Корректный словарь с районами."""
        r = RegionDataGetter(db_session_full)
        results = r.get_unique_districts()
        assert len(results) == len(
            self.UNIQUE_DISTRICTS), 'Кол-во районов не совпадает'
        for district in self.UNIQUE_DISTRICTS:
            assert district in results
        assert 'октябрьский' not in results
        assert results['ижморский'] == 42

    def test_get_unique_towns_ok(self, db_session_full):
        """Корректный словарь с городами."""
        r = RegionDataGetter(db_session_full)
        results = r.get_unique_towns()
        assert len(results) == len(
            self.UNIQUE_TOWNS), 'Кол-во городов не совпадает'
        for town in self.UNIQUE_TOWNS:
            assert town in results
        assert 'советск' not in results
        assert results['шуя'] == 37

    def test_get_unique_localities_ok(self, db_session_full):
        """Корректный словарь с населенными пунктами."""
        r = RegionDataGetter(db_session_full)
        results = r.get_unique_localities()
        assert len(results) == len(
            self.UNIQUE_LOCALITIES), 'Кол-во населенных пунктов не совпадает'
        for locality in self.UNIQUE_LOCALITIES:
            assert locality in results
        assert 'иваново' not in results
        assert results['подовинное'] == 74

    def test_get_ps_prefixes(self, db_session_full):
        """Корректный словарь с почтовыми префиксами."""
        r = RegionDataGetter(db_session_full)
        results = r.get_ps_prefixes()
        assert len(results) == len(
            self.PS_PREFIXES), 'Кол-во префиксов почтовых индекс не совпадает'
        for ps_prefix in self.PS_PREFIXES:
            assert ps_prefix in results
        assert '679' not in results
        assert results['125'] == 77

    def test_get_all_data(self, db_session_full):
        """Корректный словарь с результатами основного метода класса."""
        r = RegionDataGetter(db_session_full)
        results = r.get_all_data()

        for key in self.DICT_KEYS:
            assert key in results

        for reg_id in self.REGION_IDS:
            assert reg_id in results["regions"]
        for alias in self.ALIASES:
            assert alias in results["aliases"]
        for district in self.UNIQUE_DISTRICTS:
            assert district in results["districts"]
        for town in self.UNIQUE_TOWNS:
            assert town in results["towns"]
        for locality in self.UNIQUE_LOCALITIES:
            assert locality in results["localities"]
        for ps_prefix in self.PS_PREFIXES:
            assert ps_prefix in results["ps_prefixes"]


class TestRegionFinderWithKVr:
    """Класс TestRegionFinderWithKV используется для
    тестирования корректности определения регионов в адресной строке.

    """
