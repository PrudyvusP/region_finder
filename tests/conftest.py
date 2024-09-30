import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from region_finder.models import Address, Alias, Base, Region, Town

addresses = [
    Address(postcode='692910', area=None, locality='находка', region_id=25),
    Address(postcode='188824', area='выборгский', locality='поляны',
            region_id=47),
    Address(postcode='361308', area='урванский', locality='урвань',
            region_id=7),
    Address(postcode='629700', area='ямальский', locality='яр-сале',
            region_id=89),
    Address(postcode='655619', area=None, locality='саяногорск', region_id=19),
    Address(postcode='652131', area='ижморский', locality='берикуль',
            region_id=42),
    Address(postcode='125039', area=None, locality=None, region_id=77),
    Address(postcode='153000', area=None, locality='иваново', region_id=37),
    Address(postcode='182165', area='великолукский', locality='иваново',
            region_id=60),
    Address(postcode='456805', area=None, locality='верхний уфалей',
            region_id=74),
    Address(postcode='457173', area='октябрьский', locality='подовинное',
            region_id=74),
    Address(postcode='692561', area='октябрьский', locality='покровка',
            region_id=25),
]

regions = [
    Region(name='Ленинградская область', region_id=47,
           aliases=[Alias(name='ленинградская')]),
    Region(name='Кемеровская область - Кузбасс', region_id=42,
           aliases=[Alias(name='кемеровская'),
                    Alias(name='кузбасс')]),
    Region(name='Приморский край', region_id=25,
           aliases=[Alias(name='приморский')]),
    Region(name='Москва', region_id=77,
           aliases=[Alias(name='москва')]),
    Region(name='Республика Хакасия', region_id=19,
           aliases=[Alias(name='хакасия')]),
    Region(name='Кабардино-Балкарская Республика', region_id=7,
           aliases=[Alias(name='кабардино-балкарская')]),
    Region(name='Ямало-Ненецкий автономный округ', region_id=89,
           aliases=[Alias(name='ямало-ненецкий')]),
    Region(name='Ивановская область', region_id=37,
           aliases=[Alias(name='ивановская')]),
    Region(name='Псковская область', region_id=60,
           aliases=[Alias(name='псковская')]),
    Region(name='Челябинская область', region_id=74,
           aliases=[Alias(name='челябинская')]),
    Region(name='Калининградская область', region_id=39,
           aliases=[Alias(name='калининградская')]),
    Region(name='Кировская область', region_id=43,
           aliases=[Alias(name='кировская')]),
]

towns = [
    Town(name='губкинский', region_id=89),
    Town(name='фурманов', region_id=37),
    Town(name='шуя', region_id=37),
    Town(name='советск', region_id=43),
    Town(name='советск', region_id=39),
]


@pytest.fixture(scope='session')
def engine():
    engine = create_engine("sqlite://", echo=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def db_session(engine):
    connection = engine.connect()
    Base.metadata.create_all(engine)
    session = Session(bind=connection)
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    connection.close()


@pytest.fixture(scope='function')
def db_session_empty(db_session):
    yield db_session
    db_session.rollback()


@pytest.fixture(scope="module")
def db_session_full(db_session):
    for region in regions:
        db_session.add(region)

    for address in addresses:
        db_session.add(address)

    for town in towns:
        db_session.add(town)

    db_session.commit()
    yield db_session


@pytest.fixture
def address_factory():
    def _make_address(postcode=None, locality=None, region_id=None, area=None):
        return Address(postcode=postcode, locality=locality,
                       region_id=region_id, area=area)

    return _make_address


@pytest.fixture
def region_factory():
    def _make_region(region_id=None, name=None, aliases=[]):
        return Region(region_id=region_id, name=name,
                      aliases=aliases)

    return _make_region


@pytest.fixture
def town_factory():
    def _make_town(region_id=None, name=None):
        return Town(region_id=region_id, name=name)

    return _make_town


@pytest.fixture
def alias_factory():
    def _make_alias(region_id=None, name=None):
        return Alias(region_id=region_id, name=name)

    return _make_alias


@pytest.fixture
def primor_kray_addr(address_factory):
    return address_factory(postcode='692910', locality='находка', region_id=25,
                           area='советский')


@pytest.fixture
def primor_kray_region(region_factory):
    return region_factory(name='Приморский край', region_id=25,
                          aliases=[Alias(name='приморский')])


@pytest.fixture
def primor_kray_town(town_factory):
    return town_factory(name='находка', region_id=25)


@pytest.fixture
def primor_kray_alias(alias_factory):
    return alias_factory(name='приморский', region_id=25)
