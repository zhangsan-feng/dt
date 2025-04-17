
from sqlmodel import SQLModel, Field, create_engine


class DownLoadTaskEntity(SQLModel, table=True):
    __tablename__ = "download_tasks"
    id: int = Field(primary_key=True)
    link:str
    nickname:str
    user_id: str
    status: int  # 0 1
    total:int
    update_time:str
    platform:str

sqlite_url = "sqlite:///store.db"
engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)