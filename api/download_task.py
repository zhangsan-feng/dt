from datetime import datetime
from sqlmodel import Session, select
from fastapi import Request
from entity.download_task_entity import engine, DownLoadTaskEntity





async def download_task_query():
    with Session(engine) as session:
        statement = select(DownLoadTaskEntity)
        results = session.exec(statement).all()
        return results



async def download_task_del(request: Request):
    json_body = await request.json()
    id = json_body["id"]
    with Session(engine) as session:
        task = session.get(DownLoadTaskEntity, id)
        if task:
            session.delete(task)
            session.commit()
            return {"code":200,"data": "delete success", "msg": ""}
        return {"code":500,"data": "error", "msg": ""}


async def download_task_update(id, user_id, status, total, platform):
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



async def download_task_add(request: Request):
    json_body = await request.json()
    link = json_body["link"]
    nickname = json_body.get("nickname", "")
    user_id = json_body.get("user_id", "")

    with Session(engine) as session:


        existing_task = session.exec(
            select(DownLoadTaskEntity)
            .where(DownLoadTaskEntity.link == link)
        ).first()
        if existing_task:
            return {"code":500,"data": "link exist", "msg": ""}

        download_task = DownLoadTaskEntity(
            link=link,
            nickname=nickname if nickname else "",
            user_id=user_id if user_id else "",
            status=0,
            total=0,
            platform="",
            update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        session.add(download_task)
        session.commit()
        session.refresh(download_task)
        return {"code":200,"data": "success", "msg": ""}