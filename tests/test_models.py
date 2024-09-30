import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from region_finder.models import Address, Alias, Region, Town


class TestModel:
    """Тестирование моделей.

    Методы
    -------
    check_valid_table_name():
        .
    add_instance_and_commit():
        .

    test_valid_tablename_region():
        .
    test_valid_tablename_address():
        .
    test_valid_tablename_town():
        .
    test_valid_tablename_alias():
        .
    test_add_valid_region():
        .
    test_add_valid_address():
        .
    test_add_valid_alias():
        .
    test_add_valid_town():
        .
    test_orm_relationships():
        .
    test_add_region_wo_name():
        .
    test_add_address_wo_region_id():
        .
    test_add_alias_wo_name():
        .
    test_add_alias_wo_region_id():
        .
    test_add_town_wo_name():
        .
    test_add_town_wo_region_id():
        .
    test_add_double_region_id():
        .
    """

    @staticmethod
    def check_valid_table_name(model, name):
        """Проверяет атрибут __table__ модели model
        на соответствие переданному name."""
        assert getattr(model, '__tablename__') == name

    @staticmethod
    def add_instance_and_commit(session, instance):
        """Добавляет переданную сущность instance в
        session и сохраняет изменения в бд."""
        session.add(instance)
        session.commit()

    def test_valid_tablename_region(self):
        """Корректное название таблицы regions."""
        self.check_valid_table_name(Region, 'regions')

    def test_valid_tablename_address(self):
        """Корректное название таблицы addresses."""
        self.check_valid_table_name(Address, 'addresses')

    def test_valid_tablename_town(self):
        """Корректное название таблицы towns."""
        self.check_valid_table_name(Town, 'towns')

    def test_valid_tablename_alias(self):
        """Корректное название таблицы aliases."""
        self.check_valid_table_name(Alias, 'aliases')

    def test_add_valid_region(self, db_session_empty, primor_kray_region):
        """Корректное добавление региона."""
        db_session_empty.add(primor_kray_region)
        query = select(Region).where(Region.name == 'Приморский край')
        region = db_session_empty.scalars(query).first()
        assert region.region_id == 25
        assert str(region) == '<Region Приморский край>'

    def test_add_valid_address(self, db_session_empty, primor_kray_addr):
        """Корректное добавление адреса."""
        db_session_empty.add(primor_kray_addr)
        query = select(Address).where(Address.postcode == '692910')
        address = db_session_empty.scalars(query).first()
        assert address.region_id == 25
        assert address.area == 'советский'
        assert address.locality == 'находка'
        assert str(address) == '<Address 692910>'

    def test_add_valid_alias(self, db_session_empty, primor_kray_alias):
        """Корректное добавление алиаса региона."""
        db_session_empty.add(primor_kray_alias)
        query = select(Alias).where(Alias.name == 'приморский')
        alias = db_session_empty.scalars(query).first()
        assert alias.region_id == 25
        assert str(alias) == '<Alias приморский>'

    def test_add_valid_town(self, db_session_empty, primor_kray_town):
        """Корректное добавление города."""
        db_session_empty.add(primor_kray_town)
        query = select(Town).where(Town.name == 'находка')
        town = db_session_empty.scalars(query).first()
        assert town.region_id == 25
        assert str(town) == '<Town находка>'

    def test_orm_relationships(self, db_session_empty, primor_kray_region,
                               primor_kray_addr, primor_kray_town):
        """Корректное использование связей на уровне ORM."""
        db_session_empty.add_all([primor_kray_region,
                                  primor_kray_addr, primor_kray_town])

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
    def test_add_region_wo_name(self, db_session_empty, region_factory):
        """Попытка добавить регион без обязательного поля name."""
        self.add_instance_and_commit(
            db_session_empty, region_factory(region_id=1))

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_address_wo_region_id(self, db_session_empty, address_factory):
        """Попытка добавить адрес без обязательного поля region_id."""
        self.add_instance_and_commit(db_session_empty,
                                     address_factory(postcode='111111'))

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_alias_wo_name(self, db_session_empty, alias_factory):
        """Попытка добавить алиас региона без обязательного поля name."""
        self.add_instance_and_commit(db_session_empty, alias_factory(
            region_id=25))

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_alias_wo_region_id(self, db_session_empty,
                                    alias_factory):
        """Попытка добавить алиас региона без обязательного поля region_id."""
        self.add_instance_and_commit(db_session_empty,
                                     alias_factory(name='приморский'))

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_town_wo_name(self, db_session_empty, town_factory):
        """Попытка добавить город без обязательного поля name."""
        self.add_instance_and_commit(db_session_empty,
                                     town_factory(region_id=25))

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_town_wo_region_id(self, db_session_empty,
                                   town_factory):
        """Попытка добавить город без обязательного поля region_id."""
        self.add_instance_and_commit(db_session_empty,
                                     town_factory(name='находка'))

    @pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_double_region_id(self, db_session_empty, region_factory):
        """Попытка добавить два региона с одинаковым region_id."""
        r1 = region_factory(name='Москва', region_id=77)
        r2 = region_factory(name='Москва', region_id=77)
        self.add_instance_and_commit(db_session_empty, r1)
        self.add_instance_and_commit(db_session_empty, r2)
