import re
from datetime import datetime
from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask

class TestTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试"

    def run(self):
        self.test()

    def test(self):
        # self.checkColor(0.86,0.79, targetRgb=(67, 5, 8))
        # self.checkColor(0.86,0.79, targetRgb=(78, 53, 41))
        self.checkColor(0.87,0.80, targetRgb=(75, 34, 9))
        self.checkColor(0.87,0.56, targetRgb=(230, 209, 140))
