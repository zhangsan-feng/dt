from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, Column, Text
from application.entity import engine

class CookieToConfigEntyty(SQLModel, table=True):
    __tablename__ = "config_cookies"
    config_id: int = Field(default=None, sa_column=Column(Integer))
    cookies_id: int = Field(default=None, sa_column=Column(Integer))


class CookiesEntity(SQLModel, table=True):
    __tablename__ = "cookies"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    cookie: str = Field(sa_column=Column(Text))


# print(CreateTable(ConfigEntity.__table__).compile(engine))
SQLModel.metadata.create_all(engine)


async def cookies_add(config_id, cookie):
    pass

async def cookies_delete(config_id):
    pass

async def cookies_update(config_id, cookie):
    pass

async def cookies_query(config_id):
    pass
