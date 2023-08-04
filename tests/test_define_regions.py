"""
@pytest.fixture(scope='module')
def db():
    db = ...
    db.connect()
    yield db
    db.close()


def test_data_from_db(db):
    ...

@pytest.fixture(scope='module')
def test_region():
    test_region = Region('')
"""