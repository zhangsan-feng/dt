import os
from application.entity.config_enetity import config_query_


class Config:
    def __init__(self):
        config_ = config_query_()
        self.project_path: str = config_.project_path
        self.save_path: str = config_.save_path
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)

        self.douyin_cookie: str = config_.douyin_cookie if config_.douyin_cookie else ""
        self.bilibili_cookie: str = config_.bilibili_cookie if config_.bilibili_cookie else ""
        self.hongshu_cookie: str = config_.hongshu_cookie if config_.hongshu_cookie else ""
        self.weibo_cookie: str = config_.weibo_cookie if config_.weibo_cookie else ""
        self.kuaishou_cookie: str = config_.kuaishou_cookie if config_.kuaishou_cookie else ""

        self.douyin_path = self.save_path + "douyin"
        if not os.path.exists(self.douyin_path): os.makedirs(self.douyin_path)

        self.bilibili_path = self.save_path + "bilibili"
        if not os.path.exists(self.bilibili_path): os.makedirs(self.bilibili_path)

        self.hongshu_path = self.save_path + "/hongshu/"
        if not os.path.exists(self.hongshu_path): os.makedirs(self.hongshu_path)
        #
        # self.weibo_path = self.save_path + "/weibo/"
        # if not os.path.exists(self.weibo_path): os.makedirs(self.weibo_path)
        #
        # self.kuaishou_path = self.save_path + "/kuaishou/"
        # if not os.path.exists(self.kuaishou_path): os.makedirs(self.kuaishou_path)

        self.proxy: str = config_.proxy
        self.update_time: str = config_.update_time

        self.host = "127.0.0.1"
        self.port = 8000
        self.address = self.host + ":" + str(self.port)
        self.resource_path = "http://" + self.address + "/download/"

        self.only_audio = config_.only_audio if config_.only_audio else False
        self.only_video = config_.only_video if config_.only_video else False
        self.only_image = config_.only_image if config_.only_image else False

        self.max_download_num = 100

    def get_cookie(self, platform):
        pass

    def get_proxy(self):
        pass

    def is_download_max(self, file_path):
        directory  = os.path.dirname(file_path)
        mp3_count = sum(1 for f in os.listdir(directory) if f.lower().endswith('.mp3'))
        mp4_count = sum(1 for f in os.listdir(directory) if f.lower().endswith('.mp4'))

        return max(mp3_count, mp4_count) > self.max_download_num