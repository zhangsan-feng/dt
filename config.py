import os
from application.entity.config_enetity import config_query_

class Config:
    def __init__(self):
        config_ = config_query_()
        self.project_path: str = config_.project_path
        self.save_path: str = config_.save_path
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)
        self.douyin_cookie: str = config_.douyin_cookie
        self.douyin_path = self.save_path + "/douyin/"
        if not os.path.exists(self.douyin_path): os.makedirs(self.douyin_path)

        self.bilibili_path = self.save_path + "/bilibili/"
        if not os.path.exists(self.bilibili_path): os.makedirs(self.bilibili_path)

        self.proxy: str = config_.proxy
        self.update_time: str = config_.update_time

        self.host = "127.0.0.1"
        self.port = 8000
        self.address = self.host + ":" + str(self.port)
        self.resource_path = "http://" + self.address + "/download/"


