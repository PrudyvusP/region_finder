import pytest

from region_finder.models import Region
from region_finder.rfinder_alch_kv import RegionFinderWithKV, RegionDataGetter

class TestRegionDataGetter:
    """Класс TestRegionDataGetter используется для
         тестирования правильности отдачи подготовительных данных,
         необходимых для поиска регионов.

    Методы
    -------
    test_get_regions()
    """

    def test_get_regions(self, db_session_empty, lots_regions):
        r = RegionDataGetter(db_session_empty)
        db_session_empty.bulk_save_objects(lots_regions)
        results = r.get_regions()
        assert len(results) == 10
        assert 19 in results


