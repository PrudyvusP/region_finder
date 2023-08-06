from sqlalchemy import select

from region_finder.models import Region


class TestRegionFinderWithSQLADB:

    def test_region_valid(self, db_session, valid_region):
        db_session.add(valid_region)
        query = select(Region).where(Region.name == 'Архангельская область')
        arhangelsk = db_session.scalars(query).first()
        assert arhangelsk.region_id == 29
