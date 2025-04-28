
from sqlalchemy import create_engine
engine = create_engine("sqlite:///store.db")
# engine = create_engine("duckdb:///database.duckdb")