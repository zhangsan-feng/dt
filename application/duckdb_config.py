
import duckdb

class DuckDBConfigure:

    def __init__(self, db_name='database.duckdb', **config_kwargs):
        if hasattr(self, 'connection') and self.connection is not None:
            return

        self.db_name = db_name
        self.connection = None
        self.config = {
            'threads': 8,
            'memory_limit': '5GB',
            'max_memory': '512MB',
            'default_order': 'DESC',
            'default_null_order': 'NULLS LAST',
            **config_kwargs
        }

    def init_connection(self):
        if self.connection is None:
            self.connection = duckdb.connect(
                database=self.db_name,
                config=self.config
            )

    def init_duckdb(self):
        self.init_connection()
        try:

            print(f"Database '{self.db_name}' initialized successfully.")

            self.connection.sql("""

            CREATE SEQUENCE IF NOT EXISTS config_id_seq START 1;
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY DEFAULT nextval('config_id_seq'),
                project_path VARCHAR,
                save_path VARCHAR,
                proxy VARCHAR,
                douyin_cookie TEXT,
                hongshu_cookie TEXT,
                bilibili_cookie TEXT,
                kuaishou_cookie TEXT,
                weibo_cookie TEXT,
                update_time TIMESTAMP WITHOUT TIME ZONE
            );

            CREATE SEQUENCE IF NOT EXISTS download_task_id_seq START 1;
            CREATE TABLE IF NOT EXISTS download_task (
                id INTEGER PRIMARY KEY DEFAULT nextval('download_task_id_seq'),

            );

            CREATE SEQUENCE IF NOT EXISTS download_record_id_seq START 1;
            CREATE TABLE IF NOT EXISTS download_record (
                id INTEGER PRIMARY KEY DEFAULT nextval('download_record_id_seq'),
            );
            """)
            self.connection.commit()
            self.close_connection()

        except Exception as e:
            print(f"Failed to initialize database: {e}")
            raise

    def get_connection(self):
        if self.connection is None:
            self.init_connection()
        return self.connection

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                # print(f"Database '{self.db_name}' closed successfully.")
            except Exception as e:
                print(f"Failed to close database: {e}")

    def exec(self, sql):
        self.init_connection()
        res = self.connection.execute(sql).fetchall()
        self.connection.commit()
        self.close_connection()
        return res