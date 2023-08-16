from sqlalchemy.orm import Session

from create_tables import engine

session = Session(bind=engine)
