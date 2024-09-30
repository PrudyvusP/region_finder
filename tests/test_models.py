import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from region_finder.models import Address, Alias, Region, Town


class TestModel:
    """Тестирование моделей."""

    @staticmethod
    def check_valid_table_name(model, name):
        """Проверяет атрибут __table__ модели model
        на соответствие переданному name."""
        assert getattr(model, '__tablename__') == name

    @staticmethod
    def add_invalid_instance(session, instance):

        session.add(instance)
        session.commit()

    def test_valid_tablename_region(self):
        """Корректное название таблицы regions."""
        self.check_valid_table_name(Region, 'regions')

    def test_valid_tablename_address(self):
        """Корректное название таблицы addresses."""
        self.check_valid_table_name(Address, 'addresses')

    def test_valid_table_name_town(self):
        """Корректное название таблицы towns."""
        self.check_valid_table_name(Town, 'towns')

    def test_valid_table_name_alias(self):
        """Корректное название таблицы aliases."""
        self.check_valid_table_name(Alias, 'aliases')

    def test_add_valid_region(self, db_session_empty, one_region):
        """Корректное добавление региона."""
        db_session_empty.add(one_region)
        query = select(Region).where(Region.name == 'Приморский край')
        region = db_session_empty.scalars(query).first()
        assert region.region_id == 25
        assert str(region) == '<Region Приморский край>'

    def test_add_valid_address(self, db_session_empty, one_address):
        """Корректное добавление адреса."""
        db_session_empty.add(one_address)
        query = select(Address).where(Address.postcode == '692910')
        address = db_session_empty.scalars(query).first()
        assert address.region_id == 25
        assert address.area == 'советский'
        assert address.locality == 'находка'
        assert str(address) == '<Address 692910>'

    def test_add_valid_alias(self, db_session_empty, one_alias):
        """Корректное добавление алиаса региона."""
        db_session_empty.add(one_alias)
        query = select(Alias).where(Alias.name == 'приморский')
        alias = db_session_empty.scalars(query).first()
        assert alias.region_id == 25
        assert str(alias) == '<Alias приморский>'

    def test_add_valid_town(self, db_session_empty, one_town):
        """Корректное добавление города."""
        db_session_empty.add(one_town)
        query = select(Town).where(Town.name == 'находка')
        town = db_session_empty.scalars(query).first()
        assert town.region_id == 25
        assert str(town) == '<Town находка>'

    def test_orm_relationships(self, db_session_empty, one_region,
                               one_address, one_town):
        """Корректное использование ORM-relationship."""
        db_session_empty.add_all([one_region, one_address, one_town])

        r_query = select(Region).where(Region.name == 'Приморский край')
        region = db_session_empty.scalars(r_query).first()
        a_query = select(Alias).where(Alias.name == 'приморский')
        alias = db_session_empty.scalars(a_query).first()
        addr_query = select(Address).where(Address.postcode == '692910')
        address = db_session_empty.scalars(addr_query).first()
        t_query = select(Town).where(Town.name == 'находка')
        town = db_session_empty.scalars(t_query).first()

        assert region.aliases == [alias]
        assert alias.region == region
        assert address.region == region
        assert region.addresses == [address]
        assert town.region == region
        assert region.towns == [town]

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_region(self, db_session_empty, region_wo_name):
        """Попытка добавить регион без обязательного поля name."""
        self.add_invalid_instance(db_session_empty, region_wo_name)

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_address(self, db_session_empty, address_wo_region_id):
        """Попытка добавить адрес без обязательного поля region_id."""
        self.add_invalid_instance(db_session_empty, address_wo_region_id)

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_alias_name(self, db_session_empty, alias_wo_name):
        """Попытка добавить алиас региона без обязательного поля name."""
        self.add_invalid_instance(db_session_empty, alias_wo_name)

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_alias_region_id(self, db_session_empty,
                                         alias_wo_region_id):
        """Попытка добавить алиас региона без обязательного поля region_id."""
        self.add_invalid_instance(db_session_empty, alias_wo_region_id)

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_alias_name(self, db_session_empty, town_wo_name):
        """Попытка добавить город без обязательного поля name."""
        self.add_invalid_instance(db_session_empty, town_wo_name)

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_alias_region_id(self, db_session_empty,
                                         town_wo_region_id):
        """Попытка добавить город без обязательного поля region_id."""
        self.add_invalid_instance(db_session_empty, town_wo_region_id)
