from sqlalchemy import select

from region_finder.models import Address, Alias, Region


class TestRegionFinderWithSQLADB:

    def test_valid_table_names(self):
        """Корректные названия таблиц."""

        assert Region.__tablename__ == 'regions'
        assert Address.__tablename__ == 'addresses'
        assert Alias.__tablename__ == 'aliases'

    def test_valid_region(self, db_session):
        """Корректное добавление региона."""

        valid_region = Region(
            name='Архангельская область',
            region_id=29)
        db_session.add(valid_region)
        query = select(Region).where(Region.name == 'Архангельская область')
        region = db_session.scalars(query).first()
        assert region.region_id == 29
        assert str(region) == '<Region Архангельская область>'

    def test_valid_address(self, db_session):
        """Корректное добавление адреса."""

        valid_address = Address(
            postcode='164567',
            area='холмогорский',
            locality='заполье',
            region_id=29)
        db_session.add(valid_address)
        query = select(Address).where(Address.postcode == '164567')
        address = db_session.scalars(query).first()
        assert address.region_id == 29
        assert address.area == 'холмогорский'
        assert address.locality == 'заполье'
        assert str(address) == '<Address 164567>'

    def test_valid_alias(self, db_session):
        """Корректное добавление алиаса региона."""

        valid_alias = Alias(
            name='архангельская',
            region_id=29)
        db_session.add(valid_alias)
        query = select(Alias).where(Alias.name == 'архангельская')
        alias = db_session.scalars(query).first()
        assert alias.region_id == 29
        assert str(alias) == '<Alias архангельская>'

    def test_orm_relationships(self, db_session):
        """Корректное использование ORM-relationship."""

        r_query = select(Region).where(Region.name == 'Архангельская область')
        region = db_session.scalars(r_query).first()
        a_query = select(Alias).where(Alias.name == 'архангельская')
        alias = db_session.scalars(a_query).first()
        addr_query = select(Address).where(Address.postcode == '164567')
        address = db_session.scalars(addr_query).first()

        assert region.aliases == [alias]
        assert alias.region == region
        assert address.region == region
        assert region.addresses == [address]
