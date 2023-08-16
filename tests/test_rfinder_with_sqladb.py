from region_finder.rfinder_with_sqladb import RegionFinderWithSQLADB


class TestRegionFinderWithSQLADB:

    def test_define_region(self, db_session):
        s = RegionFinderWithSQLADB('Архангельская область', session=db_session)
        print(s.define_regions())
        assert len(s.define_regions()) > 0
