import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from region_finder.models import Base, Region


@pytest.fixture(scope='session')
def engine():
    return create_engine("sqlite://", echo=True)


@pytest.fixture(scope='session')
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, create_tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='module')
def valid_region():
    valid_region = Region(
        name='Архангельская область',
        region_id=29
    )
    return valid_region
