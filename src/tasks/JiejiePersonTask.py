from ok import Logger
logger = Logger.get_logger(__name__)
from src.tasks.MyBaseTask import MyBaseTask

class JiejiePersonTask(MyBaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "结界突破"
        self.description = "默认打9退四"

    def run(self):
        self.log_info('开始循环结界突破!')
        breakTroughPerson(self)

def getClickBtnPos(self, times):
    x = 0.25
    y = 0.25
    # donex = 0.29
    # doney = 0.2
    # donex1 = 0.37
    # doney1 = 0.34
    donex = 0.25
    doney = 0.225
    # 第一排
    if times < 4:
        x = times * x
        donex = times * donex
    # 第二排
    if times >= 4 and times < 7:
        x = (times - 3) * x
        donex = (times - 3) * donex
        y += 0.2
        doney += 0.19
    # 第三排
    if times >= 7 and times < 10:
        x = (times - 6) * x
        donex = (times - 6) * donex
        y += 0.4
        doney += 0.38
    print(f'getClickBtnPos x{x} y{y} donex{donex} doney{doney}')

    # alreadyAttack = self.findOcr(donex, doney, donex1, doney1, match='破')
    alreadyAttack = self.checkColor(donex, doney, rgb=(109,102,94))
    if alreadyAttack:
        return True
    self.clickRandom(x,y)
    return False

def useAllTicket(self):
    if self.findOcr(0.89,0.01, match='0/30', fullMatch=True):
        self.exitPage()
        self.log_info('已经消耗完所有的突破票!', notify=True)
        return True
    return False

def breakTroughPerson(self):
    self.closeErrorDialogWhileAttack()
    self.clickOcr(0.5,0.1,match='探索')
    # 第一轮
    timesTurn = 1
    # 第一轮 第一次
    times = 1
    state = 'ready'
    intoAttackFail = False
    needQuit = False
    quitTimes = 1
    self.clickImg(match='tansuo_liaotupo')
    # 检查是否处于结界突破界面
    if self.findImg(match='tansuo_liaotupo_yinyangliao'):
        print(f'checkColor 处于结界突破界面')
        # 30票 最多4轮
        while timesTurn <= 4:
            # 消耗完所有的突破票
            if useAllTicket(self):
                times = 10
                timesTurn = 5
                return
            self.log_info(f"🔄第 {timesTurn}/4 轮结界突破")
            times = 1
            while times <= 9:
                # 消耗完所有的突破票
                if useAllTicket(self):
                    times = 10
                    timesTurn = 5
                    return
                
                self._sleep(1)
                
                if state == 'alreadyAttack':
                    state = 'ready'

                # 攻打结界
                if state == 'ready': 
                    self.log_info(f"🔄第 {times}/9 次，第 {timesTurn} 轮结界突破")
                    # 点击结界 打开进攻弹窗
                    alreadyAttack = getClickBtnPos(self, times)
                    if alreadyAttack:
                        print(f'该结界已击破')
                        times += 1
                        state = 'alreadyAttack'
                    #　检查是否处于点击进攻的弹窗界面
                    if state == 'ready' and self.clickOcr(0,0,match='进攻'):
                        if self.findOcr(0,0,match='进攻'):
                            self.clickRandom(0.92,0.16)
                            self.clickRandom(0.92,0.16)
                            intoAttackFail = True
                        else:
                            print(f'进入战斗 waitting...')
                            state = 'waitting-attack'
                            self._sleep(3)
                            # 是否需要退4
                            if needQuit:
                                self.clickRandom(0.03,0.04, time=1)
                                self.clickOcr(0.45,0.45,match='确认')
                                times += 1
                                quitTimes += 1
                    if intoAttackFail:
                        times = 999
                # 战斗中---结束战斗
                if state == 'waitting-attack':
                    checkAttackState = self.checkAttackState()
                    if checkAttackState == 'attack_success_fudai':
                        times += 1
                        state = 'ready'
                        self._sleep(3)
                    if checkAttackState == 'attack_fail':
                        state = 'ready'
                        self._sleep(3)

                if quitTimes == 5:
                    needQuit = False
                    quitTimes = 1
                    times = 1
                if times == 4 and state == 'ready':
                    self.checkAttackState()
                    print(f'领取福袋')
                if times == 7 and state == 'ready':
                    self.checkAttackState()
                    print(f'领取福袋')
                if times == 10 and state == 'ready':
                    self.checkAttackState()
                    print(f'领取福袋')
                    print(f'打完一个轮次了')
                    needQuit = True
                    timesTurn += 1
                    self._sleep(30)