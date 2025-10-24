import re
from datetime import datetime
from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class DailyDiGuiTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "地域鬼王"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '地域鬼王打几次': 3,
        })

    def run(self):
        self.log_info('地域鬼王开始运行!', notify=True)
        self.daily_digui()
        self.log_info('地域鬼王运行完成!', notify=True)

    def daily_digui(self):
        # 是否在允许打地域鬼王的时间内 6-24点
        if self.getHour() < 6:
            self.log_info('不在地域鬼王可用时间!', notify=True)
            return
        self.clickOcr(0.5,0.1,match='探索')
        times = 1
        state = 'init'
        maxTimes = self.config.get('地域鬼王打几次')
        if self.clickImg(match='tansuo_digui', time=3):
            state = '地域鬼王首页'
        if self.findOcr(match='地域最强'):
            state = '地域鬼王首页'
        if state == '地域鬼王首页':
            while times <= maxTimes:
                print(f"🔄 尝试第 {times}/3 次地域鬼王")
                # 每秒执行一次
                self._sleep(1)
                if state == '地域鬼王首页' and self.clickImg(match='tansuo_digui_filter'):
                    state = '选择地域鬼王界面'
                if state == '选择地域鬼王界面':
                    if times == 1 and self.clickImg(match='tansuo_digui_tiaozhan'):
                        print(f"🔄 点击第1个挑战按钮")
                        state = '地域鬼王挑战开始界面'
                    if not self.checkColor(0.87,0.56, targetRgb=(230, 209, 140)) and times == 2:
                        print(f"🔄 第2个挑战按钮未解锁")
                        times = 4
                        state = '地域鬼王挑战开始界面'
                        self.exitPage()
                    if times == 2 and self.clickImg(match='tansuo_digui_tiaozhan_2', time=2):
                        print(f"🔄 点击第2个挑战按钮")
                        state = '地域鬼王挑战开始界面'
                    if not self.checkColor(0.87,0.80, targetRgb=(75, 34, 9)) and times == 3:
                        print(f"🔄 第3个挑战按钮未解锁")
                        times = 4
                        state = '地域鬼王挑战开始界面'
                        self.exitPage()
                    if times == 3 and self.clickImg(match='tansuo_digui_tiaozhan_3', time=2):
                        print(f"🔄 点击第3个挑战按钮")
                        state = '地域鬼王挑战开始界面'
                if state == '地域鬼王挑战开始界面':
                    if self.clickImg(match='tansuo_digui_tiaozhan_start', time=5) or self.clickOcr(0.86,0.73,match='挑战',time=5):
                        state = '战斗中'
                        self.clickImg(match='attack_ready')
                        self._sleep(10)
                if state == '战斗中':
                    if self.checkAttackState() == 'attack_success_fudai':
                        state = '战斗结束'
                        times += 1
                        self._sleep(5)
                        self.exitPage()
                        state = '地域鬼王首页'
        self.clickRandom(0.05,0.07, time=5)
        self.exitPage()
        print(f" 打完三次地鬼，回到庭院首页 ")