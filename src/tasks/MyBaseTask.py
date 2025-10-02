import random
import re

from ok import BaseTask
from ok import Logger
logger = Logger.get_logger(__name__)
class MyBaseTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 公共方法
    def operate(self, func):
        self.executor.interaction.operate(func, block=True)

    def do_mouse_down(self, key):
        self.executor.interaction.do_mouse_down(key=key)

    def do_mouse_up(self, key):
        self.executor.interaction.do_mouse_up(key=key)

    def do_send_key_down(self, key):
        self.executor.interaction.do_send_key_down(key)

    def do_send_key_up(self, key):
        self.executor.interaction.do_send_key_up(key)
    
    def wait_find_box_by_ocr(self, x1, y1, tox, toy, match):
        box_list = self.wait_ocr(x1, y1, tox, toy, match=match, log=True, settle_time=1, raise_if_not_found=True)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            logger.info(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            logger.info(f"  相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            logger.info(f"❌ 未找到匹配 '{match}' 的Box")
            return None
        
    def find_box_by_ocr(self, x1, y1, tox, toy, match):
        box_list = self.ocr(x1, y1, tox, toy, match=match, log=True)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            logger.info(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            logger.info(f"  相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            logger.info(f"❌ 未找到匹配 '{match}' 的Box")
            return None
        
    def find_box_by_cv(self, x, y, to_x, to_y, match):
        box_list = self.find_feature(match)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            logger.info(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            logger.info(f"  相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            logger.info(f"❌ 未找到匹配 '{match}' 的Box")
            return None
        
    def getRound(self, base=0, min=0.1, max=0.6, fixed=1):
        result = base + random.uniform(min, max)
        return round(result, fixed)

    def pressKeyRandom(self, key):
        down_time = self.getRound(0.2)
        self.send_key(key, down_time)

    def click_box_area_random(self, box, margin=5):
        """在Box区域内完全随机点击（避免边缘）
        
        Args:
            box: Box对象
            margin: 距离边缘的最小像素
        """
        if not box:
            return False
        
        # 计算可点击区域（避开边缘）
        min_x = box.x + margin
        max_x = box.x + box.width - margin
        min_y = box.y + margin
        max_y = box.y + box.height - margin
        
        # 确保有有效的点击区域
        if min_x >= max_x or min_y >= max_y:
            # 如果区域太小，使用中心点
            target_x, target_y = box.center()
        else:
            # 在有效区域内随机选择
            target_x = random.randint(int(min_x), int(max_x))
            target_y = random.randint(int(min_y), int(max_y))
        
        
        down_time = self.getRound(0.2)

        logger.info(f"🎯 区域随机点击: ({target_x}, {target_y}, {down_time})")
        self.click(target_x, target_y, down_time)
        return True

    def click_box_relative_random(self, box, x, y, screen_width=1280, screen_height=720):
        """使用相对坐标的随机点击（适合不同分辨率）
        
        Args:
            box: Box对象
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        if box:
            x_center, y_center = box.center()
            x_percent = x_center / screen_width
            y_percent = y_center / screen_height
        elif x > 0:
            x_percent = x
            y_percent = y
        else:
            return False
        
        # 在相对坐标基础上添加随机偏移
        x_offset_percent = self.getRound(0,0.005,0.01, 3)  # ±1%的随机偏移
        y_offset_percent = self.getRound(0,0.005,0.01, 3)
        
        final_x_percent = x_percent + x_offset_percent
        final_y_percent = y_percent + y_offset_percent
        
        # 确保在有效范围内
        final_x_percent = max(0.0, min(1.0, final_x_percent))
        final_y_percent = max(0.0, min(1.0, final_y_percent))
        
        logger.info(f"   基础相对坐标: ({x_percent:.4f}, {y_percent:.4f})")
        logger.info(f"   最终相对坐标: ({final_x_percent:.4f}, {final_y_percent:.4f})")
        
        down_time = self.getRound()
        self.click(final_x_percent, final_y_percent, down_time)
        return True
    
    def clickRandom(self, x, y, time=1):
        self.click_box_relative_random(None,x,y)
        if (time > 0):
            self._sleep(time)

    def clickRandomBox(self, box, time=1):
        self.click_box_area_random(box)
        if (time > 0):
            self._sleep(time)

    def closeErrorDialog(self):
        # if (self.clickImg('')):
            # self._sleep(1)
            logger.info(f"closeErrorDialog ")

    def exitPage(self):
        self.pressKeyRandom('esc')
        self._sleep(1)
    
    # 外层api

    def findOcr(self, x1 = 0, y1 = 0, tox = 1, toy = 1, match = ""):
        box = self.find_box_by_ocr(x1, y1, tox, toy, match)
        return box

    def clickOcr(self, x1 = 0, y1 = 0, tox = 1, toy = 1, match = "", time = 1):
        box = self.find_box_by_ocr(x1, y1, tox, toy, match)
        if (box):
            self.clickRandomBox(box, time)
            return box
        else:
            return None

    def clickImg(self, x1 = 0, y1 = 0, tox = 1, toy = 1, match = "", time = 1):
        box = self.find_box_by_cv(x1, y1, tox, toy, match)
        if (box):
            self.clickRandomBox(box, time)
            return box
        else:
            return None

    def _sleep(self, time = 1):
        timemin = min(1, time + 0.5)
        timemax = max(1, time + 1)
        timerandom = random.randint(timemin, timemax)
        logger.info(f" wait '{timerandom}' second")
        self.sleep(timerandom)
        self.closeErrorDialog()