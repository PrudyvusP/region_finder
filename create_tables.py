from sqlalchemy import create_engine

from region_finder.models import Base

engine = create_engine("sqlite:///test.db", echo=False)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
