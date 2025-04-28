from sqlalchemy.sql.ddl import CreateTable
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column, Text, desc
from application.entity import engine


class RecordEntity(SQLModel, table=True):
    __tablename__ = "record"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    aweme_id:str = Field(default=None, sa_column=Column(String))
    author: str = Field(default=None, sa_column=Column(String))
    author_id: str = Field(default=None, sa_column=Column(String))
    desc: str = Field(default=None, sa_column=Column(Text))
    files: str = Field(default=None, sa_column=Column(Text))


# print(CreateTable(RecordEntity.__table__).compile(engine))
# SQLModel.metadata.create_all(engine)

async def record_add(obj):
    with Session(engine) as session:
        session.add(RecordEntity(**obj))
        session.commit()


async def record_query(page=1):
    with Session(engine) as session:
        results = session.exec(
            select(RecordEntity)
            .order_by(desc(RecordEntity.id))
            .offset(page - 1 * 100)
            .limit(100)
        ).all()
        # print(results)
        return results

async def record_delete(id):
    with Session(engine) as session:
        task = session.get(RecordEntity, id)
        if task:
            session.delete(task)
            session.commit()