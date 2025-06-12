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


class ConfigEntityObject:
    def __init__(self, ):
        # print(CreateTable(ConfigEntity.__table__).compile(engine))
        SQLModel.metadata.create_all(engine)

        current_file_path = os.path.abspath(__file__)
        project_dir = os.path.dirname(current_file_path)
        project_dir = os.path.dirname(project_dir)
        project_dir = os.path.dirname(project_dir).replace("\\", "/")
        # print(f"工作目录: {project_dir}")

        with Session(engine) as session:
            with Session(engine) as session:
                model = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
                if not model:
                    value = ConfigEntity(
                        project_path=project_dir,
                        save_path=project_dir + "/download/",
                        update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )

                    session.add(value)
                    session.commit()
                    session.refresh(value)

            config_ = self.query()
            self.project_path: str = config_.project_path
            self.save_path: str = config_.save_path
            if not os.path.exists(self.save_path): os.makedirs(self.save_path)

            self.douyin_cookie: str = config_.douyin_cookie if config_.douyin_cookie else ""
            self.bilibili_cookie: str = config_.bilibili_cookie if config_.bilibili_cookie else ""
            self.hongshu_cookie: str = config_.hongshu_cookie if config_.hongshu_cookie else ""
            self.weibo_cookie: str = config_.weibo_cookie if config_.weibo_cookie else ""
            self.kuaishou_cookie: str = config_.kuaishou_cookie if config_.kuaishou_cookie else ""

            self.douyin_path = self.save_path + "douyin"
            if not os.path.exists(self.douyin_path): os.makedirs(self.douyin_path)

            self.bilibili_path = self.save_path + "bilibili"
            if not os.path.exists(self.bilibili_path): os.makedirs(self.bilibili_path)

            self.hongshu_path = self.save_path + "hongshu"
            if not os.path.exists(self.hongshu_path): os.makedirs(self.hongshu_path)

            # self.weibo_path = self.save_path + "/weibo/"
            # if not os.path.exists(self.weibo_path): os.makedirs(self.weibo_path)
            #
            # self.kuaishou_path = self.save_path + "/kuaishou/"
            # if not os.path.exists(self.kuaishou_path): os.makedirs(self.kuaishou_path)

            self.proxy: str = config_.proxy
            self.update_time: str = config_.update_time

            self.host = "127.0.0.1"
            self.port = 8000
            self.address = self.host + ":" + str(self.port)
            self.resource_path = "http://" + self.address + "/download/"

            self.only_audio = True
            self.only_video = False
            self.only_image = False
            self.download_limit_num = 300
            self.download_limit = False
            self.download_format = True
            self.download_filter = False
            self.download_delay = True
            self.download_delay_num = 1.5

    def get_cookie(self, platform):
        pass

    def get_proxy(self):
        pass




    def query(self):
        with Session(engine) as session:
            results = session.exec(select(ConfigEntity).where(ConfigEntity.id == 1)).first()
            # print(results)
            return results

    def edit(self, obj):
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
                model.proxy = obj["proxy"] if "proxy" in obj else ""

                model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session.add(model)
                session.commit()


