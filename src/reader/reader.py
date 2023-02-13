import logging
import sys

import pandas as pd
from config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

logging.basicConfig(level=logging.DEBUG)  # TODO: make configurable

db_params = Config().dict()
db_url = URL.create(**db_params)
logging.debug(db_url)

engine = create_engine(db_url)

query = '''SELECT country, COUNT(*) 
           FROM people 
           INNER JOIN places 
           ON people.place_of_birth = places.city 
           GROUP BY country'''

try:
    with engine.connect() as conn:
        df = pd.read_sql(text(query), con=conn, index_col='country').squeeze()
        df.to_json('/data/summary_output.json')  # TODO: don't hardcode file path
except (DBAPIError, SQLAlchemyError) as sqlaerr:
    logging.error(sqlaerr)
    sys.exit(1)
