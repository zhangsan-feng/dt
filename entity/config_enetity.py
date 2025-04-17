import json
import os



class ConfigEntity:
    def __init__(self, save_path):
        self.save_path = save_path
        self.proxy = None

        self.douyin_cookie = None
        self.douyin_path = self.save_path + "/douyin/"

        self.bilibili_cookie = None
        self.bilibili_path = self.save_path + "/bilibili/"

        self.weibo_cookie = None
        self.weibo_path = self.save_path + "/bilibili/"

        self.kuaishou_cookie = None
        self.kuaishou_path = self.save_path + "/bilibili/"

        if not os.path.exists(self.save_path): os.makedirs(self.save_path)
        if not os.path.exists(self.douyin_path): os.makedirs(self.douyin_path)
        if not os.path.exists(self.douyin_path): os.makedirs(self.weibo_path)
        if not os.path.exists(self.douyin_path): os.makedirs(self.kuaishou_path)

        if not os.path.exists("./config.json"): return

        with open("./config.json", "r", encoding="utf-8") as f:
            json_config = json.loads(f.read())

        # self.logger.info(json.dumps(json_config, indent=4, ensure_ascii=False))
        self.douyin_cookie = json_config["douyin_cookie"]


    def platform(self, str_platform):
        if str_platform == "douyin":
            return self.douyin_path

config = ConfigEntity("../download")




