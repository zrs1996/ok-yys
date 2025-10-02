import re

from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class YuhunTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "御魂"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
            'list选项': ['第一', '第二', '第3'],
        })
        self.config_type["下拉菜单选项"] = {'type': "drop_down",
                                      'options': ['第一', '第二', '第3']}

    def run(self):
        self.log_info('日常任务开始运行!', notify=True)
        self.log_info('日常任务运行完成!', notify=True)