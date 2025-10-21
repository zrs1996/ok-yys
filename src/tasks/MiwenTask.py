import re
from datetime import datetime
from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class MiwenTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "周常秘闻副本"
        self.description = "用户点击时调用run方法"
        
    def run(self):
        self.log_info('周常秘闻副本开始运行!', notify=True)
        self.week_miwen()
        self.log_info('周常秘闻副本运行完成!', notify=True)

    def week_miwen(self):
        self.clickOcr(0.5,0.1,match='探索')
        self.clickOcr(match='秘闻副本')
        self.clickOcr(match='秘闻挑战开启')
        self.clickOcr(0.7,0.7,match='进入')
        count = 1
        while self.findOcr(0.2,0.89,match='总耗时尚未通关'):
            self.sleep(1)
            if self.clickOcr(0.7,0.7,match='挑战', time=3):
                state = '进入挑战'
                self.clickImg(match='attack_ready', time=1)
                self.clickRandom(0.28,0.59)
                while state != '战斗结束':
                    self.sleep(1)
                    if self.clickOcr(0.3,0.2,match='通关阵容'):
                        count = count + 1
                        state = '战斗结束'
        if self.findOcr(0.7,0.7,match='挑战'):
            self.exitPage()
        if self.findOcr(0.7,0.7,match='进入'):
            self.exitPage()