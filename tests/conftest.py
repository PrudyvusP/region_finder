import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from region_finder.models import Base, Region, Alias, Address

addresses = [
    Address(postcode='692910', locality='находка', region_id=25),
    Address(postcode='188824', area='выборгский', locality='поляны',
            region_id=47),
    Address(postcode='361308', area='урванский', locality='урвань',
            region_id=7),
    Address(postcode='629700', area='ямальский', locality='яр-сале',
            region_id=89),
    Address(postcode='655619', locality='саяногорск', region_id=19),
    Address(postcode='652131', area='ижморский', locality='берикуль',
            region_id=42),
    Address(postcode='125039', region_id=77),
    Address(postcode='111923', region_id=77),
    Address(postcode='153000', locality='иваново', region_id=37),
    Address(postcode='153950', locality='иваново', region_id=37),
    Address(postcode='182165', area='великолукский', locality='иваново',
            region_id=60),
    Address(postcode='456805', locality='верхний уфалей',
            region_id=74),

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

]


@pytest.fixture(scope='session')
def engine():
    return create_engine("sqlite://", echo=False)


@pytest.fixture(scope="module")
def db_session(engine):
    connection = engine.connect()
    Base.metadata.create_all(engine)
    session = Session(bind=connection)
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
    connection.close()


@pytest.fixture(scope="module")
def db_session_with_data(db_session):
    db_session.add_all(regions)
    db_session.add_all(addresses)
    db_session.commit()
    yield db_session
