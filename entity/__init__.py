# import duckdb
#
# conn = duckdb.connect(
#     database='store.duckdb',
#     config={
#         'threads': 4,
#         'memory_limit': '5GB',
#         'max_memory': '512MB',
#         'default_order': 'DESC',
#         'default_null_order': 'NULLS LAST'
#     }
# )
#
# conn.sql("""
#
# CREATE SEQUENCE IF NOT EXISTS config_id_seq START 1;
# CREATE TABLE IF NOT EXISTS config (
#     id INTEGER PRIMARY KEY DEFAULT nextval('config_id_seq'),
#     project_path VARCHAR,
#     save_path VARCHAR,
#     douyin_cookie TEXT,
#     proxy VARCHAR,
#     update_time TIMESTAMP WITHOUT TIME ZONE
# );
# """)
#
#

from sqlalchemy import create_engine
engine = create_engine("sqlite:///store.db")