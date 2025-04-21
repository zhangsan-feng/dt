from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import String, Integer, Column
from entity import engine

class DownLoadTaskEntity(SQLModel, table=True):
    __tablename__ = "download_task"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    link: str = Field(sa_column=Column(String))
    nickname: str = Field(sa_column=Column(String))
    user_id: str = Field(sa_column=Column(String))
    status: int = Field(sa_column=Column(Integer))  # 0 或 1
    total: int = Field(sa_column=Column(Integer))
    platform: str = Field(sa_column=Column(String))
    update_time: str = Field(sa_column=Column(String))

# print(CreateTable(DownLoadTaskEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)


async def task_update(user_id, status, total, platform):
    with Session(engine) as session:
        model = session.exec(select(DownLoadTaskEntity).where(DownLoadTaskEntity.id == id)).first()
        if model:
            model.user_id = user_id
            model.status = status
            model.total = total
            model.platform = platform
            model.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.add(model)
            session.commit()
            return {"code": 200, "data": "update success", "msg": ""}


async def task_delete(id):
    with Session(engine) as session:
        task = session.get(DownLoadTaskEntity, id)
        if task:
            session.delete(task)
            session.commit()
            return {"code": 200, "data": "delete success", "msg": ""}


async def task_add(link):
    with Session(engine) as session:
        existing_task = session.exec(select(DownLoadTaskEntity).where(DownLoadTaskEntity.link == link)).first()
        if existing_task:
            return {"code": 500, "data": "link exist", "msg": ""}

        download_task = DownLoadTaskEntity(
            link=link,
            nickname="NULL" ,
            user_id="NULL",
            status=0,
            total=0,
            platform="NULL",
            update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        session.add(download_task)
        session.commit()
        session.refresh(download_task)
        return {"code": 200, "data": "success", "msg": ""}

async def task_query():
    with Session(engine) as session:
        statement = select(DownLoadTaskEntity)
        results = session.exec(statement).all()
        return  {"code": 200, "data": results, "msg": ""}
