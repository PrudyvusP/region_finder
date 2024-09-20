from sqlalchemy.orm import Session

from engine import engine

session = Session(bind=engine)
