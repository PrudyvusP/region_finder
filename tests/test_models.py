from sqlalchemy import select

from region_finder.models import Region


class TestRegionFinderWithSQLADB:

    def region_valid(self, db_session, valid_region):
        db_session.add(valid_region)
        query = select(Region).where(Region.name == 'Архангельская область')
        arhangelsk = db_session.scalars(query).first()
        assert arhangelsk.region_id == 29

    def base_is_empty (self, db_session):
        assert not db_session.scalars(select(Region)).all()
