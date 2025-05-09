from datetime import datetime

from sqlalchemy.sql.ddl import CreateTable
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column
from application.entity import engine

class DownLoadBatchEntity(SQLModel, table=True):
    __tablename__ = "download_task"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    link: str = Field(sa_column=Column(String))
    author: str = Field(sa_column=Column(String))
    user_id: str = Field(sa_column=Column(String))
    status: int = Field(sa_column=Column(Integer))  # 0 或 1
    platform: str = Field(sa_column=Column(String))
    update_time: str = Field(sa_column=Column(String))

# print(CreateTable(DownLoadBatchEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)


async def batch_update(user_id, status, author, platform):
    with Session(engine) as session:
        model = session.exec(select(DownLoadBatchEntity).where(DownLoadBatchEntity.id == id)).first()
        if model:
            model.author = author
            model.user_id = user_id
            model.status = status
            model.platform = platform
            model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.add(model)
            session.commit()


async def batch_delete(id):
    with Session(engine) as session:
        task = session.get(DownLoadBatchEntity, id)
        if task:
            session.delete(task)
            session.commit()


async def batch_add(link):
    with Session(engine) as session:
        existing_task = session.exec(select(DownLoadBatchEntity).where(DownLoadBatchEntity.link == link)).first()
        if not existing_task:

            download_task = DownLoadBatchEntity(
                link=link,
                author="NULL" ,
                user_id="NULL",
                status=0,
                platform="NULL",
                update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            session.add(download_task)
            session.commit()
            session.refresh(download_task)


async def batch_query(page):
    with Session(engine) as session:
        results = session.exec(select(DownLoadBatchEntity).offset(page - 1 * 100).limit(100)).all()
        return results

async def batch_query_all():
    with Session(engine) as session:
        results = session.exec(select(DownLoadBatchEntity)).all()
        return results