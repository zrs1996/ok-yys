from ok import Logger
logger = Logger.get_logger(__name__)

from .DailyDiGuiTask import daily_digui
from src.tasks.MyBaseTask import MyBaseTask

class DailyTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常一条龙"

    def run(self):
        self.log_info('日常任务开始运行!', notify=True)
        daily_digui(self)
        self.daily_home()
        self.daily_YinYangLiao()
        self.log_info('日常任务运行完成!', notify=True)

    def daily_home(self):
        # 展开主题
        if self.clickImg(match='home_bottom_fold'):
            isExpend = True
        isEmail = self.findImg(match='home_email')
        isHome = isEmail
        if not isEmail:
            isHome = self.findOcr(match='阴阳术') or self.findOcr(match='合战')
            if not isHome:
                return
        # 领取邮件
        if isEmail:
            self.clickImg(match='home_email')
            if self.findOcr(match='邮箱'):
                self.clickOcr(match='键已读')
                if self.clickOcr(match='一键领取') or self.clickOcr(match='领取'):
                    self.clickOcr(match='确定')
                    self.exitPage()
                self.exitPage()
        # 领取签到
        if self.clickImg(match='home_qiandao'):
            self.clickOcr(match='每日一签', time=1)
            self.exitPage()
            if self.findOcr(match='累计奖励'):
                self.exitPage()
        # 领取福利签
        if self.clickImg(match='home_gift_qian'):
           self.exitPage()
        # 领取御魂觉醒加成
        if self.clickImg(match='home_gift_jiacheng'):
           self.exitPage()
        # 领取体力
        if self.clickImg(match='home_gift_tili'):
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
            if self.findOcr(match="礼包屋"):
                # 点击礼包屋
                self.clickRandom(0.91,0.93)
                if self.clickOcr(0.92,0.51,match="日常"):
                    if self.clickOcr(0.15, 0.40, match="免费"): self.exitPage()
                    self.exitPage()
                self.exitPage()
        # 免费 1/1 每日免费票
        if isHome:
            self.clickRandom(0.86,0.28)
            if self.findOcr(match='免费 1/1'):
                self.clickRandom(0.48,0.88)
                self.mouse_down(0.36,0.51)
                self.swipe_relative(0.36,0.51,0.62,0.32)
                self.mouse_up()
                self.mouse_down(0.63,0.33)
        

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
