import json
import multiprocessing
import time
import uuid
import threading

DownLoadTaskManager: dict[str, dict] = {}
rw_lock = threading.RLock()


def create_task(func, *args, **kwargs):
    task_id = str(uuid.uuid4())
    # kwargs.setdefault("task_id", task_id)

    process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
    process.start()

    with rw_lock:
        DownLoadTaskManager[task_id] = {
            "process": process,
            "author": kwargs.get("author", "Unknown"),
            "title": kwargs.get("title", "Untitled"),
            "status": "running"
        }
        print(f"Task created with ID: {task_id}")


def kill_task(task_id):
    if task_id not in DownLoadTaskManager:
        return

    task_data = DownLoadTaskManager[task_id]
    process = task_data["process"]
    with rw_lock:
        if process.is_alive():
            process.terminate()
            process.join()
            DownLoadTaskManager[task_id]["status"] = "done"


def get_task():
    task_list = []
    for task_id, task_data in DownLoadTaskManager.items():
        task_list.append(
            {
                "uuid": task_id,
                "Author": task_data["author"],
                "Title": task_data["title"],
                "Status": task_data["status"],
            }
        )

    print(json.dumps(task_list, indent=4, ensure_ascii=False))

def example_task(duration, author, title, task_id):
    print(f"Task {task_id} started by {author} with title '{title}',running for {duration} seconds...")
    time.sleep(duration)
    print("Task fished.")

if __name__ == "__main__":

    create_task(example_task, 5,  author="牛马", title="xxx")
    create_task(example_task, 10, author="马楼", title="sb")

    try:
        while True:
            get_task()
            time.sleep(3)
    except KeyboardInterrupt:
        print("Exiting program...")