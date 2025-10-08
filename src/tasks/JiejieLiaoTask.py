import re

from ok import BaseTask
from ok import find_boxes_by_name, Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class JiejieLiaoTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "寮突破"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '打第几个结界': 1,
        })

    def run(self):
        self.log_info('开始循环寮突破!')
        self.daily_liaotupo()
        # self.shutdown()

    def daily_liaotupo(self):
        self.closeErrorDialogWhileAttack()
        self.clickOcr(0.5,0.1,match='探索')
        times = 1
        self.clickImg(match='tansuo_liaotupo')
        # 检查是否处于寮突破界面
        self.clickImg(match='tansuo_liaotupo_yinyangliao')
        state = 'ready'
        resetTimes = 1
        reopen = False
        while times <= 100:
            if self.findImg(match='tansuo_liaotupo_yinyangliao_finish') or self.findOcr(0.1,0.15,match='已攻破'):
                times = 999
                self.exitPage()
                self.log_info('寮突破运行完成!', notify=True)
                return None
            if state == 'ready': 
                self.log_info(f"🔄第 {times}/100 次寮突破")
            # 检查是否处于寮突破界面
            option = self.config.get('打第几个结界')
            if self.findOcr(0.12,0.78, match='击败次数'):
                if option == 2:
                    self.clickRandom(0.7,0.23)
                else:
                    self.clickRandom(0.45,0.24)
            #　检查是否处于点击进攻的弹窗界面
            if option == 2:
                if self.clickOcr(0.75,0.5,match='进攻'):
                    self.log_info('进入战斗 wait 20 second')
                    self._sleep(5)
                    if self.findOcr(0.75,0.5,match='进攻'):
                        self.clickRandom(0.92,0.16)
                        self.clickRandom(0.92,0.16)
                        reopen = True
                        self._sleep(15)
            else:
                if self.clickOcr(0.48,0.5,match='进攻'):
                    self.log_info('进入战斗 wait 20 second')
                    self._sleep(5)
                    if self.findOcr(0.48,0.5,match='进攻'):
                        self.clickRandom(0.92,0.16)
                        self.clickRandom(0.92,0.16)
                        reopen = True
                        self._sleep(15)
            self._sleep(1)
            if reopen:
                self.clickImg(match='tansuo_liaotupo')
                # 检查是否处于寮突破界面
                if self.clickImg(match='tansuo_liaotupo_yinyangliao'):
                    reopen = False
            state = self.checkAttackState()
            if state == 'attack_success_fudai':
                times += 1
                resetTimes += 1
                state = 'ready'
                self._sleep(10)
            if state == 'attack_fail':
                resetTimes += 1
                state = 'ready'
                self._sleep(10)