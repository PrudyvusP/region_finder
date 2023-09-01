from sqlalchemy import create_engine

from region_finder.models import Base

engine = create_engine("sqlite:///test.db", echo=False)

if __name__ == '__main__':
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        print("Не удалось создать БД.")
        Base.metadata.drop_all(bind=engine)
