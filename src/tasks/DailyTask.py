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
        self.into_game()
        self.close_login_tip_jiacheng()
        self.daily_shop()
        self.daily_HuaHeZhan_Task()
        self.daily_YinYangLiao()
        self.log_info('日常任务运行完成!', notify=True)

    def daily_shop(self):
        if (self.into_Shopping()):
            self.sleep(1)
            if (self.into_Gift()):
                self.sleep(1)
                if (self.into_DailyGift()):
                    self.sleep(1)
                    if (self.ocrClick(0.15, 0.40, match="免费")):
                        self.pressKeyRandom('esc')
                    self.back_DailyGift()
                    self.sleep(1)
                    self.back_Gift()
                    self.sleep(1)
                else:
                    self.back_DailyGift()
                    self.sleep(1)
            else:
                self.back_Shopping()
                self.sleep(1)

    def daily_HuaHeZhan_Task(self):
        if (self.into_HuaHeZhan()):
            self.sleep(1)
            self.clickRandom(0.95,0.45)
            self.sleep(.5)
            if (self.into_HuaHeZhan_pick_getAll()):
                self.sleep(2)
                self.clickRandom(0.59,0.91)
                self.sleep(.5)
                self.clickRandom(0.03,0.05)
                self.sleep(.5)
            else:
                self.clickRandom(0.03,0.05)
                self.sleep(.5)
        else:
            self.clickRandom(0.03,0.05)
            self.sleep(.5)

    def daily_YinYangLiao(self):
        if (self.ocrFind(match="阴阳寮")):
            self.clickRandom(0.44,0.88)
            self.sleep(2)
            # 打开结界
            if (self.ocrClick(0.80, 0.90, match="结界")):
                self.sleep(2)
                # 打开结界卡
                self.clickRandom(0.74,0.47)
                self.sleep(1)
                # if (self.check_ActiveJiejie()):
                # self.sleep(1)
                # 打开全部
                self.clickRandom(0.34,0.17)
                self.sleep(1)
                # 选择太鼓
                self.clickRandom(0.34,0.38)
                self.sleep(1)
                # 选第一张太鼓
                self.clickRandom(0.25,0.31)
                self.sleep(1)
                # 点击激活
                self.clickRandom(0.85,0.83)
                self.sleep(1)
                # 点击确定 是否将寄养位置
                self.clickRandom(0.60, 0.60)
                self.sleep(1)
                # 关掉寄养界面
                self.clickRandom(0.92, 0.16)
                self.sleep(1)
                # 退出结界
                self.clickRandom(0.04, 0.06)
                self.sleep(2)
                # 退出阴阳寮
                self.clickRandom(0.04, 0.06)
                self.sleep(2)
            else: 
                # 退出阴阳寮
                self.clickRandom(0.04, 0.06)
                self.sleep(2)
                return None

    def into_game(self):
        box = self.find_box_by_ocr(0,0,1,1, match="进入游戏")
        if (box):
            self.clickRandomBox(box)
            self.sleep(4)
            return box

    def into_Shopping(self):
        box = self.ocrClick(0,0,1,1, match="商店")
        if (box):
            return True
        # self.clickRandom(0.54,0.89)
        # return True
        return None
    
    def back_Shopping(self):
        self.clickRandom(0.03,0.03)

    def into_Gift(self):
        box = self.find_box_by_ocr(0,0,1,1, match="礼包屋")
        if (box):
            self.clickRandomBox(box)
            return box

    def back_Gift(self):
        self.clickRandom(46,55)

    def into_DailyGift(self):
        box = self.find_box_by_ocr(0,0,1,1, match="日常")
        if (box):
            self.clickRandomBox(box)
            return box

    def back_DailyGift(self):
        self.clickRandom(37,22)

    def into_HuaHeZhan(self):
        # box = self.find_box_by_ocr(0,0,1,1, match="花合战")
        # if (box):
        #     self.clickRandomBox(box)
        self.clickRandom(0.62,0.89)
        return True

    def into_HuaHeZhan_pick_getAll(self):
        box = self.find_box_by_ocr(0.68,0.78,1,1, match="领取")
        if (box):
            self.clickRandomBox(box)
            return box
        # self.click(0.62,0.89)

    def into_Zhaohuan(self):
        box = self.find_box_by_ocr(0,0,1,1, match="召唤")
        if (box):
            self.clickRandomBox(box)
            return box
    
    def into_Explor(self):
        box = self.find_box_by_ocr(0,0,1,1, match="探索")
        if (box):
            self.clickRandomBox(box)
            return box
            
    def into_Jiejie(self):
        box = self.find_box_by_ocr(0,0,1,1, match="结界突破")
        if (box):
            self.clickRandomBox(box)
            return box
            
    def into_Jiejie_Person(self):
        box = self.find_box_by_ocr(0,0,1,1, match="个人")
        if (box):
            self.clickRandomBox(box)
            return box
            
    def into_YinYangLiao(self):
        box = self.find_box_by_ocr(0,0,1,1, match="阴阳寮")
        if (box):
            self.clickRandomBox(box)
            return box
            
    def check_ActiveJiejie(self):
        box = self.find_box_by_ocr(0,0,1,1, match="激活")
        if (box):
            self.clickRandomBox(box)
            return box
            
    def close_login_tip_jiacheng(self):
        box = self.find_box_by_ocr(0,0,1,1, match="是否打开大人之前被自动关")
        if (box):
            self.clickRandom(0.41,0.58)
            self.sleep(1)
            return box

    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right",match="进入游戏", log=True) #指定box以提高ocr速度

    def find_some_text_with_relative_box(self):
        return self.ocr(0.5, 0.5, 1, 1, match=re.compile("招"), log=True) #指定box以提高ocr速度

    def test_find_one_feature(self):
        return self.find_one('box_battle_1')

    def test_find_feature_list(self):
        return self.find_feature('box_battle_1')

    def run_for_5(self):
        self.operate(lambda: self.do_run_for_5())

    def do_run_for_5(self):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.do_mouse_down(key='right')
        self.sleep(0.1)
        self.do_mouse_up(key='right')
        self.sleep(5)
        self.do_send_key_up('w')




