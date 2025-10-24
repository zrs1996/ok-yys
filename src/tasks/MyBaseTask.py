from datetime import datetime
import random
import win32gui
import win32ui
import win32con
# import d3dshot
import numpy as np
import mss
import dxcam
import cv2
import pyautogui
import re
import os

from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT
from ctypes import wintypes

from ok import BaseTask
from ok import Logger
import json
logger = Logger.get_logger(__name__)
class MyBaseTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 数据库
    
    def Capture(self):
        hwnd = win32gui.FindWindow(None, '阴阳师-网易游戏')
        """
        后台截图指定区域
        """
        
        # 获取客户区矩形（不包含标题栏）
        client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(hwnd)
        # 转换客户区坐标为屏幕坐标
        # client_rect = win32gui.ClientToScreen(hwnd, (client_left, client_top))
        # 计算客户区在屏幕上的位置和尺寸
        # client_screen_left = client_rect[0]
        # client_screen_top = client_rect[1]
        client_width = client_right - client_left
        client_height = client_bottom - client_top
         
        x1 = 0
        y1 = 0
        x2 = client_width
        y2 = client_height
        
        # 定义常量
        SRCCOPY = 0x00CC0020
        
        # 获取窗口客户区大小
        rect = wintypes.RECT()
        windll.user32.GetClientRect(hwnd, byref(rect))
        width, height = rect.right, rect.bottom
        
        # 设置默认值
        if x2 is None:
            x2 = width
        if y2 is None:
            y2 = height
            
        # 验证区域有效性
        if x1 >= x2 or y1 >= y2 or x2 > width or y2 > height:
            raise ValueError(f"Invalid capture region: ({x1}, {y1}, {x2}, {y2}), window size: ({width}, {height})")

        # 计算区域尺寸
        region_width = x2 - x1
        region_height = y2 - y1
        
        # 获取设备上下文
        dc = windll.user32.GetDC(hwnd)
        if not dc:
            raise Exception("Failed to get device context")
            
        # 创建兼容DC和位图
        cdc = windll.gdi32.CreateCompatibleDC(dc)
        bitmap = windll.gdi32.CreateCompatibleBitmap(dc, region_width, region_height)
        
        # 选择位图到DC
        old_bitmap = windll.gdi32.SelectObject(cdc, bitmap)
        
        # 执行位块传输
        result = windll.gdi32.BitBlt(cdc, 0, 0, region_width, region_height, 
                                dc, x1, y1, SRCCOPY)
        if not result:
            raise Exception("BitBlt operation failed")
        
        # 准备缓冲区
        total_bytes = region_width * region_height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        
        # 获取位图数据
        windll.gdi32.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        
        # 清理资源
        windll.gdi32.SelectObject(cdc, old_bitmap)
        windll.gdi32.DeleteObject(bitmap)
        windll.gdi32.DeleteObject(cdc)
        windll.user32.ReleaseDC(hwnd, dc)
        
        # 转换为numpy数组并重塑
        image = np.frombuffer(buffer, dtype=np.uint8).reshape(region_height, region_width, 4)

        # 转换为 BGR 以便 OpenCV 使用
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # 获取当前脚本文件的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建相对路径
        screenshot_dir = os.path.join(current_dir, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)  # 确保目录存在
        # 保存截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.png"
        file_path = os.path.join(screenshot_dir, filename)
        cv2.imwrite(file_path, image)
        print(f" ")
        print(f"📸 后台截图成功: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
        print(f"📸 保存至: {file_path}")
        print(f" ")
        return image
    
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

    def getTime(self):
        # 获取当前时间的时分（24小时制）
        current_time = datetime.now()
        return current_time.hour, current_time.minute
    
    def getHour(self):
        # 获取当前时间的时分（24小时制）
        current_time = datetime.now()
        return current_time.hour
    
    def is_color_similar(self, color1, color2, tolerance=0):
        """判断两个颜色是否相似"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        return (abs(r1 - r2) == tolerance and 
                abs(g1 - g2) == tolerance and 
                abs(b1 - b2) == tolerance)
    
    def checkColor(self, x,y, targetRgb):
        """获取屏幕的RGB颜色值
            
        Returns:
            tuple: (r, g, b) RGB颜色值
        """
        
        # 截取屏幕并获取颜色
        screenshot = self.Capture()

        height, width, channels = screenshot.shape
        # 获取特定坐标的颜色 (x, y)
        abs_x  = int(x * width)
        abs_y = int(y * height)
        # 获取颜色 (numpy数组的索引是 [y, x])
        color_bgr = screenshot[abs_y, abs_x]
        # 转换为 RGB
        color_rgb = (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]))  # BGR -> RGB
        print(f"🎨 获取特定坐标的颜色: x {abs_x } y {abs_y} rgb {color_rgb}")

        if targetRgb and color_rgb:
            result = self.is_color_similar(color_rgb, targetRgb)
            if result:
                print(f"✅ 找到目标 {targetRgb}")
                return True
            else:
                print(f"❌ 未找到目标 实际rgb: {color_rgb} 目标rgb: {targetRgb}")
                return False
        return False
                
    def wait_find_box_by_ocr(self, x1, y1, tox, toy, match):
        box_list = self.wait_ocr(x1, y1, tox, toy, match=match, log=True, settle_time=1, raise_if_not_found=True)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            print(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            print(f"✅ 相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            print(f"❌ 未找到匹配 '{match}' 的Box")
            return None
        
    def find_box_by_ocr(self, x1, y1, tox, toy, match, fullMatch=False):
        if fullMatch:
            box_list = self.ocr(x1, y1, tox, toy, match=match, log=True)
        else:
            box_list = self.ocr(x1, y1, tox, toy, match=re.compile(match), log=True)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            print(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            print(f"✅  相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            print(f"❌ 未找到匹配 '{match}' 的Box")
            return None
        
    def find_box_by_cv(self,match,wait=False,timeout=15,time=1):
        if wait:
            self.wait_click_feature(
                match, 
                time_out=timeout, 
                settle_time=0.5, 
                after_sleep=time
            )
            return
        box_list = self.find_feature(match)
        if box_list:
            first_box = box_list[0]
            # 计算相对坐标百分比
            x_percent = first_box.x / 1280
            y_percent = first_box.y / 720
            print(f"✅ 找到目标Box: '{first_box.name}' (置信度: {first_box.confidence:.2f})")
            print(f"✅  相对百分比: ({x_percent:.3f}, {y_percent:.3f})")
            return first_box
        else:
            print(f"❌ 未找到匹配 '{match}' 的Box")
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

        print(f"🎯 区域随机点击: ({target_x}, {target_y}, {down_time})")

        self.click(target_x, target_y, down_time)
        return True

    def click_box_relative_random(self, box, x, y, screen_width=1280, screen_height=720):
        """使用相对坐标的随机点击（适合不同分辨率）
        
        Args:
            box: Box对象
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        down_time = self.getRound()

        if box:
            x_center, y_center = box.center()
            x_percent = x_center / screen_width
            y_percent = y_center / screen_height
            # 在相对坐标基础上添加随机偏移
            x_offset_percent = self.getRound(0,0.002,0.005, 3)  # ±1%的随机偏移
            y_offset_percent = self.getRound(0,0.002,0.005, 3)
        elif x > 0 and x < 1:
            x_percent = x
            y_percent = y
            # 在相对坐标基础上添加随机偏移
            x_offset_percent = self.getRound(0,0.002,0.005, 3)  # ±1%的随机偏移
            y_offset_percent = self.getRound(0,0.002,0.005, 3)
        else:
            # 在相对坐标基础上添加随机偏移
            x_offset_percent = self.getRound(0,0.002,0.005, 3)  # ±10的随机偏移
            y_offset_percent = self.getRound(0,0.002,0.005, 3)
        
        
        final_x_percent = x_percent + x_offset_percent
        final_y_percent = y_percent + y_offset_percent
        
        # 确保在有效范围内
        final_x_percent = max(0.0, min(1, final_x_percent))
        final_y_percent = max(0.0, min(1, final_y_percent))
        

        print(f"🎯 区域随机点击: ({final_x_percent:.4f}, {final_y_percent:.4f})")

        self.click(final_x_percent, final_y_percent, down_time)
        return True
    
    def clickRandom(self, x, y, time=1):
        print(f"clickRandom wait second time={time} ")
        self.click_box_relative_random(None,x,y)
        if(time > 0):
            self._sleep(time)

    def clickRandomBox(self, box, time=1):
        print(f"clickRandomBox wait second time={time} ")
        self.click_box_area_random(box)
        if(time > 0):
            self._sleep(time)

    def closeErrorDialogWhileAttack(self):
        if (self.clickImg(match='close_invite', time=0)):
            self.sleep(1)
            print(f"关闭邀请")
        if (self.findOcr(match='悬赏封印')):
            self.pressKeyRandom('esc')
            self.sleep(1)
            print(f"关闭悬赏封印")

    def closeErrorDialog(self):
        if (self.clickImg(match='close_invite')):
            self.sleep(1)
            print(f"关闭邀请")
        if (self.findOcr(match="是否打开大人之前被自动关")):
            self.clickRandom(0.41,0.58, time=0)
            print(f"关闭是否打开大人之前被自动关必提示")
            self.sleep(1)

    def exitPage(self):
        self.pressKeyRandom('esc')
        self._sleep(1)
    
    # 外层api

    def findOcr(self, x1 = 0, y1 = 0, tox = 1, toy = 1, match = "", fullMatch=False):
        box = self.find_box_by_ocr(x1, y1, tox, toy, match, fullMatch)
        return box

    def clickOcr(self, x1 = 0, y1 = 0, tox = 1, toy = 1, match = "", time = 1, fullMatch=False):
        box = self.find_box_by_ocr(x1, y1, tox, toy, match, fullMatch)
        if (box):
            self.clickRandomBox(box, time)
            return box
        else:
            return None

    def clickImg(self, match = "", timeout=15, time = 1,wait=False):
        box = self.find_box_by_cv(match,wait,time,timeout)
        if (box):
            self.clickRandomBox(box, time)
            return box
        else:
            return None
        
    def findImg(self, match = "", timeout=15, time = 1,wait=False):
        return self.find_box_by_cv(match,wait,time,timeout)

    def _sleep(self, time = 1):
        timemin = min(time, time + 0.5)
        timemax = max(1, time + 1)
        timerandom = random.randint(timemin, timemax)
        print(f" time={time} wait '{timerandom}' second")
        self.sleep(timerandom)

    def enterGame(self):
        # self.clickRandom(0.01,0.03)
        # self._sleep(3)
        if (self.findImg(match='home_enter_game')):
            print(f" 识别到处于选择账号界面 点击进入游戏 ")
            self.clickRandom(0.48,0.57)
        # self.clickOcr(match='进入游戏', time=4)

    # 识别当前的界面处于什么状态
    # 处于庭院
    # 处于探索界面
    # 处于组队挑战界面
    # 处于战斗状态
    # 处于战斗结束后的结算状态
    def checkState(self):
        if self.findImg(match='home'):
            return 'home'
        box = self.findImg(match='attack_success', time=0)
        if box:
            self._sleep(1)
            self.clickRandomBox(box, time=5)
            return 'attack_success'
        box = self.findImg(match='attack_success_fudai', time=0)
        if box:
            self._sleep(1)
            self.clickRandomBox(box, time=5)
            return 'attack_success_fudai'
        return ''

    def checkAttackState(self):
        if self.findOcr(0.02,0.8,match='自动'):
            return 'attack_auto_attacking'
        box = self.findImg(match='attack_success')
        if box:
            self.clickRandomBox(box, time=4)
            return 'attack_success'
        box = self.findImg(match='attack_success_fudai')
        if box:
            self.clickRandomBox(box, time=4)
            return 'attack_success_fudai'
        box = self.findImg(match='attack_fail')
        if box:
            self.clickRandomBox(box, time=4)
            return 'attack_fail'
        if self.findOcr(0.02,0.8,match='自') and self.findOcr(0.02,0.8,match='动'):
            return 'attack_auto_attacking'
        return ''

    def intoTansuo(self):
        return self.clickImg(match='home_tansuo', time=2)
    
    def waitAttackEnd(self):
        notEnding = True
        while notEnding:
            state = self.checkAttackState()
            if state == 'attack_success_fudai':
                notEnding = False
            self._sleep(1)

    # 立即关机
    def shutdown(self):
        os.system("shutdown /s /t 0")