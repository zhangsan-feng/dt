import os

current_file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(current_file_path)
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir).replace("\\", "/")
# print(f"工作目录: {project_dir}")

from sqlalchemy import create_engine
db_path = os.path.join(str(project_dir) + "/", "store.db").replace("\\", "/")
engine = create_engine(f"sqlite:///{db_path}")

# engine = create_engine("duckdb:///database.duckdb")