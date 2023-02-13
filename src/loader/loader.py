import logging
import sys
from pathlib import Path

import pandas as pd
from config import Config
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.orm import declarative_base

logging.basicConfig(level=logging.DEBUG)  # TODO: make configurable

Base = declarative_base()

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    given_name = Column(String(32))
    family_name = Column(String(32))
    date_of_birth = Column(String(32))
    place_of_birth = Column(String(32))

class Places(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    city = Column(String(32))
    county = Column(String(32))
    country = Column(String(32))

db_params = Config().dict()
db_url = URL.create(**db_params)
logging.debug(db_url)

engine = create_engine(db_url)

data_path = Path('/data')
dfs = {f.stem: pd.read_csv(f) for f in data_path.glob('*.csv')}

try:
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        with conn.begin():
            for name, df in dfs.items():
                df.to_sql(name, con=conn, if_exists='replace', index='id')
except (DBAPIError, SQLAlchemyError) as sqlaerr:
    logging.error(sqlaerr)
    sys.exit(1)
