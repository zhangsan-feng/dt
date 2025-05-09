import os
from datetime import datetime

from sqlalchemy.sql.ddl import CreateTable
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column, Text
from application.entity import engine


class ConfigEntity(SQLModel, table=True):
    __tablename__ = "config"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    project_path: str = Field(default=None, sa_column=Column(String))
    save_path: str = Field(default=None, sa_column=Column(String))
    douyin_cookie: str = Field(sa_column=Column(Text))
    bilibili_cookie: str = Field(sa_column=Column(Text))
    hongshu_cookie: str = Field(sa_column=Column(Text))
    weibo_cookie: str = Field(sa_column=Column(Text))
    kuaishou_cookie: str = Field(sa_column=Column(Text))
    proxy: str = Field(sa_column=Column(String))
    update_time:str = Field(sa_column=Column(String))

# print(CreateTable(ConfigEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)

current_file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(current_file_path)
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir).replace("\\", "/")
print(f"工作目录: {project_dir}")


with Session(engine) as session:
    with Session(engine) as session:
        model = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        if not model:
            value = ConfigEntity(
                project_path = project_dir,
                save_path = project_dir + "/download/",
                update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(value)
            session.commit()
            session.refresh(value)


def config_edit_(obj):

    with Session(engine) as session:
        model = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        if not "download" in obj["save_path"]:
            if obj["save_path"][-1] == "/":
                obj["save_path"] = obj["save_path"] + "download/"
            else:
                obj["save_path"] = obj["save_path"] + "/download/"

        if model:
            model.save_path = obj["save_path"]
            model.douyin_cookie = obj["douyin_cookie"] if "douyin_cookie" in obj else ""
            model.bilibili_cookie = obj["bilibili_cookie"] if "bilibili_cookie" in obj else ""
            model.hongshu_cookie = obj["hongshu_cookie"] if "hongshu_cookie" in obj else ""
            model.weibo_cookie = obj["weibo_cookie"] if "weibo_cookie" in obj else ""
            model.kuaishou_cookie = obj["kuaishou_cookie"] if "kuaishou_cookie" in obj else ""
            model.proxy = obj["proxy"]
            model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.add(model)
            session.commit()

def config_query_():

    with Session(engine) as session:
        results = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
        # print(results)
        return results