import os
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy import String, Integer, Column, Text
from sqlmodel import Session, select
from entity import engine


class ConfigEntity(SQLModel, table=True):
    __tablename__ = "config"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    project_path: str = Field(default=None, sa_column=Column(String))
    save_path: str = Field(default=None, sa_column=Column(String))
    douyin_cookie: str = Field(sa_column=Column(Text))
    proxy: str = Field(sa_column=Column(String))
    update_time:str = Field(sa_column=Column(String))


# print(CreateTable(ConfigEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    with Session(engine) as session:
        model = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        if not model:
            current_file_path = os.path.abspath(__file__)
            project_dir = os.path.dirname(os.path.dirname(current_file_path)).replace("\\", "/")
            # print(f"项目目录: {project_dir}")

            value = ConfigEntity(
                project_path = project_dir,
                save_path = project_dir + "/download",
                douyin_cookie = "NULL",
                proxy = "NULL",
                update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(value)
            session.commit()
            session.refresh(value)


def config_edit_(obj):
    with Session(engine) as session:
        model = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        if model:
            model.project_path = obj["project_path"]
            model.save_path = obj["save_path"]
            model.douyin_cookie = obj["douyin_cookie"]
            model.proxy = obj["proxy"]
            model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.add(model)
            session.commit()

def config_query_():
    with Session(engine) as session:
        results = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        # print(results)
        return results