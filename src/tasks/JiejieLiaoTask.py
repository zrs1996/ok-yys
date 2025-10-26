from ok import Logger
logger = Logger.get_logger(__name__)

from src.tasks.MyBaseTask import MyBaseTask


class JiejieLiaoTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "寮突破"
        self.description = "用户点击时调用run方法"
        self.default_config.update({
            '从第几个结界开始打': 1,
            '打完自动关机': True,
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
                option = self.config.get('打完自动关机')
                if option: self.shutdown()
                return None
            # '击败次数：0/6'
            if self.findOcr(0.12,0.78, match='击败次数：0/6'):
                # 计算不同时间段 恢复6次所需的时间 最大30分钟
                self._sleep(30*60)
            option = self.config.get('从第几个结界开始打')
            # 检查是否处于寮突破界面
            if state == 'ready': 
                self.log_info(f"🔄第 {times}/100 次寮突破")
                if self.findOcr(0.12,0.78, match='击败次数'):
                    if option == 2:
                        self.clickRandom(0.7,0.23)
                    else:
                        self.clickRandom(0.45,0.24)
                #　检查是否处于点击进攻的弹窗界面
                if option == 2:
                    if self.clickOcr(0.75,0.5,match='进攻'):
                        self._sleep(1)
                        if self.findOcr(0.75,0.5,match='进攻'):
                            self.clickRandom(0.92,0.16)
                            self.clickRandom(0.92,0.16)
                            reopen = True
                        else:
                            self.log_info('进入战斗 waitting...')
                            state = 'waitting-attack'
                            self._sleep(5)
                else:
                    if self.clickOcr(0.48,0.5,match='进攻'):
                        self._sleep(1)
                        if self.findOcr(0.48,0.5,match='进攻'):
                            self.clickRandom(0.92,0.16)
                            self.clickRandom(0.92,0.16)
                            reopen = True
                        else:
                            self.log_info('进入战斗 waitting...')
                            state = 'waitting-attack'
                            self._sleep(5)
                if reopen:
                    self.clickImg(match='tansuo_liaotupo')
                    # 检查是否处于寮突破界面
                    if self.clickImg(match='tansuo_liaotupo_yinyangliao'):
                        reopen = False
            self._sleep(1)
            state = self.checkAttackState()
            if state == 'attack_success_fudai':
                times += 1
                resetTimes += 1
                state = 'ready'
                self._sleep(3)
            if state == 'attack_fail':
                resetTimes += 1
                state = 'ready'
                self._sleep(3)