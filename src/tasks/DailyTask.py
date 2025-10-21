import re
from datetime import datetime
from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class DailyTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常一条龙"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '地域鬼王打几次': 3,
        })

    def run(self):
        self.log_info('日常任务开始运行!', notify=True)
        self.daily_digui()
        self.clickImg(match='home_bottom_fold')
        self.daily_home()
        self.daily_YinYangLiao()
        self.week_miwen()
        self.log_info('日常任务运行完成!', notify=True)

    def daily_home(self):
        # 领取邮件
        if self.findImg(match='home_huahezhan'):
            self.clickRandom(0.90,0.06)
            if self.findOcr(match='选择一封邮件'):
                self.clickRandom(0.25,0.21, time=0)
                if self.clickOcr(match='部领取') or self.clickOcr(match='领取'):
                    self.clickOcr(match='确定')
                    self.exitPage()
                    self.exitPage()
        # 签到
        if self.clickImg(match='home_qiandao'):
            self.clickOcr(match='每日一签', time=1)
            self.exitPage()
        # 领取勾玉
        if self.clickImg(match='home_gouyu', time=2):
            self.exitPage()
        # 领取花合战任务经验
        if self.clickImg(match='home_huahezhan',time=2):
            # 点击进入任务tab
            self.clickImg(match="home_huahezhan_task",time=2)
            # 点击领取-领取花合战任务经验
            if self.clickOcr(0.68,0.78,match="领取", time=2): self.clickRandom(0.59,0.91)
            #退出花合战
            if self.findOcr(match='花合战'):
                self.clickRandom(0.03,0.05)
        # 领取商店每日福利
        if self.clickImg(match='home_shop'):
            if self.clickOcr(match="礼包屋"):
                if self.clickOcr(0.92,0.51,match="日常"):
                    if self.clickOcr(0.15, 0.40, match="免费"): self.exitPage()
                    self.exitPage()
                self.exitPage()

    def daily_YinYangLiao(self):
        if self.clickOcr(match="阴阳寮", time=2):
            # 集体任务
            if self.clickOcr(match='集体任务'):
                state = ''
                while state != '高级觉醒':
                    self.sleep(1)
                    if self.findOcr(0.15,0.25,0.3,0.31,match='高级觉醒'):
                        state = '高级觉醒'
                        self.clickOcr(0.18,0.65,0.3,0.8,match='提交')
                        self.mouse_down(0.55,0.73)
                        self.swipe_relative(0.55,0.73,0.74,0.74)
                        self.mouse_up()
                        if self.clickOcr(0.45,0.84,match='提交'):
                            self.exitPage()
                            self.exitPage()
                        self.exitPage()
                    else:
                        self.clickRandom(0.34,0.69)
            # 打开结界
            if (self.clickImg(match="yinyangliao_jiejie", time=2)):
                # 领取单式神经验
                if self.clickOcr(match='EXP'):
                    self.exitPage()
                # 领取结界卡收益
                self.clickRandom(0.71,0.24)
                # 领取体力收益
                # self.clickRandom(0.65,0.63)
                # # 取出
                # self.clickRandom(0.50,0.74)
                # self.exitPage()
                # self.exitPage()
                # 领取经验收益
                self.clickRandom(0.72,0.63)
                # 取出
                self.clickRandom(0.50,0.67)
                self.exitPage()
                # 打开结界卡
                self.clickRandom(0.74,0.47)
                if (self.findOcr(0.7, 0.8, match='卸下')):
                    # 关掉寄养界面
                    self.exitPage()
                    # 退出结界
                    self.exitPage()
                    # 退出阴阳寮
                    self.clickRandom(0.04, 0.06, 2)
                    return None
                # 打开全部
                self.clickRandom(0.34,0.17)
                # 选择太鼓
                self.clickRandom(0.34,0.38)
                # 选第一张太鼓
                self.clickRandom(0.25,0.31)
                # 点击激活
                self.clickRandom(0.85,0.83)
                # 点击确定 是否将寄养位置 设为私立/公开
                self.clickRandom(0.60, 0.60)
                # 关掉寄养界面
                self.exitPage()
                # 退出结界
                self.exitPage()
                # 退出阴阳寮
                self.clickRandom(0.04, 0.06, 2)
                return None
            else: 
                # 退出阴阳寮
                self.clickRandom(0.04, 0.06, 2)
                return None
    
    def back_Shopping(self):
        self.clickRandom(0.03,0.03)

    def back_Gift(self):
        self.clickRandom(46,55)

    def back_DailyGift(self):
        self.clickRandom(37,22)

    def test(self):
        self.clickImg(match='tansuo_digui_tiaozhan_start', time=2)
        self.clickOcr(0.86,0.73,match='挑战',time=2)

    def daily_digui(self):
        # 是否在允许打地域鬼王的时间内 6-24点
        if self.getHour() < 6:
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
                logger.info(f"🔄 尝试第 {times}/3 次地域鬼王")
                # 每秒执行一次
                self._sleep(1)
                if state == '地域鬼王首页' and self.clickImg(match='tansuo_digui_filter'):
                    state = '选择地域鬼王界面'
                if state == '选择地域鬼王界面':
                    if times == 1 and self.clickImg(match='tansuo_digui_tiaozhan'):
                        logger.info(f"🔄 点击第1个挑战按钮")
                        state = '地域鬼王挑战开始界面'
                    if times == 2 and self.clickImg(match='tansuo_digui_tiaozhan_2', time=2):
                        logger.info(f"🔄 点击第2个挑战按钮")
                        state = '地域鬼王挑战开始界面'
                    if times == 3 and self.findImg(match='tansuo_digui_tiaozhan_3_notallowed'):
                        logger.info(f"🔄 第3个挑战按钮未解锁")
                        times = 4
                        state = '地域鬼王挑战开始界面'
                        self.exitPage()
                    if times == 3 and self.clickImg(match='tansuo_digui_tiaozhan_3', time=2):
                        logger.info(f"🔄 点击第3个挑战按钮")
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
        logger.info(f" 打完三次地鬼，回到庭院首页 ")

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
        self.exitPage()