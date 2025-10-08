import re

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
        # self.enterGame()
        self.closeErrorDialog()
        self.daily_digui()
        return
        self.daily_shop()
        self.daily_HuaHeZhan_Task()
        self.daily_YinYangLiao()
        self.log_info('日常任务运行完成!', notify=True)

    def daily_shop(self):
        if (self.clickImg(match='home_shop')):
            if (self.clickOcr(0.87,0.94,1,1, match="礼包屋")):
                if (self.clickOcr(0.92,0.51,1,1, match="日常")):
                    if self.clickOcr(0.15, 0.40, match="免费"): self.exitPage()
                    #退出礼包屋
                    self.exitPage()
                    #退出商店
                    self.exitPage()
            else:
                #退出商店
                self.exitPage()

    def daily_HuaHeZhan_Task(self):
        if (self.clickImg(0.5,0.7,match='home_huahezhan',time=2)):
            self.clickImg(0.93,0.45,match="home_huahezhan_task")
            if self.clickOcr(0.68,0.78,1,1, match="领取", time=2): self.clickRandom(0.59,0.91)
            #退出花合战
            self.clickRandom(0.01,0.03)

    def daily_YinYangLiao(self):
        if (self.findOcr(match="阴阳寮")):
            self.clickRandom(0.44,0.88,2)
            # 打开结界
            if (self.clickImg(match="yinyangliao_jiejie", time=2)):
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

    def daily_digui(self):
        # if self.intoTansuo():
        if self.clickOcr(0.5,0.1,match='探索'):
            if self.clickImg(match='tansuo_digui', time=3):
                times = 1
                while times <= 3:
                    logger.info(f"🔄 尝试第 {times}/3 次地域鬼王")
                    self.clickImg(match='tansuo_digui_filter')
                    if self.findImg(match='tansuo_digui_tiaozhan'):
                        if times == 1:
                            # 点击第一个挑战按钮
                            self.clickRandom(0.72,0.34, time=2)
                            if self.clickImg(match='tansuo_digui_tiaozhan_start'):
                                self._sleep(10)
                                self.clickImg(match='attack_ready')
                                self._sleep(20)
                        if times == 2:
                            # 点击第2个挑战按钮
                            self.clickRandom(0.80,0.56, time=2)
                            if self.clickImg(match='tansuo_digui_tiaozhan_start'):
                                self._sleep(10)
                                self.clickImg(match='attack_ready')
                                self._sleep(20)
                        if times == 3:
                            # 点击第3个挑战按钮
                            self.clickRandom(0.82,0.77, time=2)
                            if self.clickImg(match='tansuo_digui_tiaozhan_start'):
                                self._sleep(10)
                                self.clickImg(match='attack_ready')
                                self._sleep(20)
                    self._sleep(1)
                    if self.checkAttackState() == 'attack_success_fudai':
                        times += 1
                        self._sleep(10)
                        self.exitPage()
        self.clickRandom(0.04,0.05, time=5)
        self.exitPage()
        logger.info(f" 打完三次地鬼，回到庭院首页 ")