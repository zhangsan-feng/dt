from datetime import datetime

from sqlalchemy.sql.ddl import CreateTable
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column
from application.entity import engine

class DownLoadTaskEntity(SQLModel, table=True):
    __tablename__ = "download_task"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    link: str = Field(sa_column=Column(String))
    author: str = Field(sa_column=Column(String))
    user_id: str = Field(sa_column=Column(String))
    status: int = Field(sa_column=Column(Integer))  # 0 或 1
    platform: str = Field(sa_column=Column(String))
    update_time: str = Field(sa_column=Column(String))

# print(CreateTable(DownLoadTaskEntity.__table__).compile(engine))
# SQLModel.metadata.create_all(engine)


async def task_update(user_id, status, author, platform):
    with Session(engine) as session:
        model = session.exec(select(DownLoadTaskEntity).where(DownLoadTaskEntity.id == id)).first()
        if model:
            model.author = author
            model.user_id = user_id
            model.status = status
            model.platform = platform
            model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.add(model)
            session.commit()


async def task_delete(id):
    with Session(engine) as session:
        task = session.get(DownLoadTaskEntity, id)
        if task:
            session.delete(task)
            session.commit()


async def task_add(link):
    with Session(engine) as session:
        existing_task = session.exec(select(DownLoadTaskEntity).where(DownLoadTaskEntity.link == link)).first()
        if not existing_task:

            download_task = DownLoadTaskEntity(
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


async def task_query():
    with Session(engine) as session:
        statement = select(DownLoadTaskEntity)
        results = session.exec(statement).all()
        return results