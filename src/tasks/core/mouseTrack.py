from pynput import mouse
import threading
import time

class AdvancedMouseTracker:
    def __init__(self):
        self.current_position = (0, 0)
        self.is_tracking = False
        self.listener = None
    
    def on_move(self, x, y):
        """鼠标移动事件回调"""
        self.current_position = (x, y)
        print(f"鼠标移动: X={x}, Y={y}")
    
    def on_click(self, x, y, button, pressed):
        """鼠标点击事件回调"""
        action = "按下" if pressed else "释放"
        print(f"鼠标{action}: {button} 在位置 ({x}, {y})")
    
    def start_tracking(self):
        """开始实时跟踪"""
        self.is_tracking = True
        
        # 创建鼠标监听器
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        
        print("开始实时鼠标跟踪 (按Esc停止)")
        self.listener.start()
        self.listener.join()  # 阻塞直到停止
    
    def stop_tracking(self):
        """停止跟踪"""
        if self.listener:
            self.listener.stop()
        self.is_tracking = False
        print("鼠标跟踪已停止")
    
    def get(self):
        """获取当前鼠标位置"""
        return self.current_position



tracker = AdvancedMouseTracker()
def init():
    tracking_thread = threading.Thread(target=tracker.start_tracking)
    tracking_thread.start()

def get():
    if tracker.is_tracking:
        return tracker.get()
    return None

def stop():
    tracker.stop_tracking()