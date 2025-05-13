from sqlalchemy.sql.ddl import CreateTable
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column, Text, desc, or_, and_
from application.entity import engine


class DownLoadRecordEntity(SQLModel, table=True):
    __tablename__ = "record"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    aweme_id:str = Field(default=None, sa_column=Column(String))
    author: str = Field(default=None, sa_column=Column(String))
    author_id: str = Field(default=None, sa_column=Column(String))
    desc: str = Field(default=None, sa_column=Column(Text))
    files: str = Field(default=None, sa_column=Column(Text))


# print(CreateTable(DownLoadRecordEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)

async def record_add(obj):
    with Session(engine) as session:
        if obj["aweme_id"] != "NULL":
            session.add(DownLoadRecordEntity(**obj))
            session.commit()
        else :
            existing_task = session.exec(select(DownLoadRecordEntity).where(DownLoadRecordEntity.aweme_id == obj["aweme_id"])).first()
            if not existing_task:
                session.add(DownLoadRecordEntity(**obj))
                session.commit()


async def record_query(page):
    with Session(engine) as session:
        results = session.exec(
            select(DownLoadRecordEntity)
            .order_by(desc(DownLoadRecordEntity.id))
            .offset((page - 1 )* 100)
            .limit(100)
        ).all()
        # print(results)
        return results


async def record_delete(id):
    with Session(engine) as session:
        task = session.get(DownLoadRecordEntity, id)
        if task:
            session.delete(task)
            session.commit()

async def record_clean():
    with Session(engine) as session:
        session.exec("DELETE FROM record;")
        session.exec("DELETE FROM sqlite_sequence WHERE name='record';")  # 重置自增ID
        session.commit()

async def record_search(key_word):
    with Session(engine) as session:
        query = select(DownLoadRecordEntity)

        conditions = []
        conditions.append(or_(
            DownLoadRecordEntity.author.contains(key_word),
            DownLoadRecordEntity.desc.contains(key_word)
        ))

        if conditions:
            query = query.where(and_(*conditions))

        result = session.exec(query)
        return result.all()