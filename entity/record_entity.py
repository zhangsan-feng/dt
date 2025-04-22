import os
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy import String, Integer, Column, Text
from sqlmodel import Session, select
from entity import engine


class RecordEntity(SQLModel, table=True):
    __tablename__ = "record"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    aweme_id:int = Field(default=None, sa_column=Column(String))
    author: str = Field(default=None, sa_column=Column(String))
    author_id: int = Field(default=None, sa_column=Column(Integer))
    desc: str = Field(default=None, sa_column=Column(Text))
    files: str = Field(default=None, sa_column=Column(Text))


# print(CreateTable(ConfigEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)

async def record_add(obj):
    with Session(engine) as session:
        session.add(RecordEntity(**obj))
        session.commit()


async def record_query():
    with Session(engine) as session:
        results = session.exec(select(RecordEntity)).all()
        # print(results)
        return results

async def record_delete(id):
    with Session(engine) as session:
        task = session.get(RecordEntity, id)
        if task:
            session.delete(task)
            session.commit()