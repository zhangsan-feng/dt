from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import String, Integer, Column, Text, desc, or_, and_, text
from application.entity import engine


class UserEntity(SQLModel, table=True):
    __tablename__ = "user"
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    name: str = Field(default=None, sa_column=Column(String))
    link: str = Field(default=None, sa_column=Column(String))
    uid: str = Field(default=None, sa_column=Column(String))
    aid: str = Field(default=None, sa_column=Column(String))
    bid: str = Field(default=None, sa_column=Column(String))
    cid: str = Field(default=None, sa_column=Column(String))
    head: str = Field(default=None, sa_column=Column(String))
    desc: str = Field(default=None, sa_column=Column(Text))
    follow: str = Field(default=None, sa_column=Column(Text))
    followed: str = Field(default=None, sa_column=Column(Text))
    works: str = Field(default=None, sa_column=Column(Text))
    is_live: bool = Field(default=None, sa_column=Column(Text))
    is_home: bool = Field(default=None, sa_column=Column(Text))

SQLModel.metadata.create_all(engine)


class UserEntityObject:

    def query(self):
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def update(self, id:int, obj:UserEntity):
        pass
