import os

import numpy as np
from ok import ConfigOption

version = "dev"

key_config_option = ConfigOption('Game Hotkey Config', { #全局配置示例
    'Echo Key': 'q',
    'Liberation Key': 'r',
    'Resonance Key': 'e',
    'Tool Key': 't',
}, description='In Game Hotkey for Skills')


def make_bottom_right_black(frame):
    """
    Changes a portion of the frame's pixels at the bottom right to black.

    Args:
        frame: The input frame (NumPy array) from OpenCV.

    Returns:
        The modified frame with the bottom-right corner blackened.  Returns the original frame
        if there's an error (e.g., invalid frame).
    """
    try:
        height, width = frame.shape[:2]  # Get height and width

        # Calculate the size of the black rectangle
        black_width = int(0.13 * width)
        black_height = int(0.025 * height)

        # Calculate the starting coordinates of the rectangle
        start_x = width - black_width
        start_y = height - black_height

        # Create a black rectangle (NumPy array of zeros)
        black_rect = np.zeros((black_height, black_width, frame.shape[2]), dtype=frame.dtype)  # Ensure same dtype

        # Replace the bottom-right portion of the frame with the black rectangle
        frame[start_y:height, start_x:width] = black_rect

        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame

config = {
    'debug': True,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'global_configs': [key_config_option],
    'screenshot_processor': make_bottom_right_black, # 在截图的时候对frame进行修改, 可选
    'gui_icon': 'icons/icon.png',
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0.2,
    'ocr': {
        'lib': 'onnxocr',
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {  # required  when supporting windows game
        'exe': 'onmyoji.exe',
        # 'hwnd_class': 'UnrealWindow', #增加重名检查准确度
        'interaction': 'Genshin', #支持大多数PC游戏后台点击
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        'bit_blt_render_full': True,
        'check_hdr': True, #当用户开启AutoHDR时候提示用户, 但不禁止使用
        'force_no_hdr': False, #True=当用户开启AutoHDR时候禁止使用
        'require_bg': True # 要求使用后台截图
    },
    'start_timeout': 120,  # default 60
    'window_size': { #ok-script窗口大小
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
    'supported_resolution': {
        'ratio': '16:9', #支持的游戏分辨率
        'min_size': (1280, 720), #支持的最低游戏分辨率
        'resize_to': [(1280, 720)], #如果非16:9自动缩放为 resize_to
    },
    'analytics': {
        'report_url': 'http://report.ok-script.cn:8080/report', #上报日活, 可选
    },
    'links': {
            'default': {
                'github': 'https://github.com/ok-oldking/ok-script-boilerplate',
                'discord': 'https://discord.gg/vVyCatEBgA',
                'sponsor': 'https://www.paypal.com/ncp/payment/JWQBH7JZKNGCQ',
                'share': 'Download from https://github.com/ok-oldking/ok-script-boilerplate',
                'faq': 'https://github.com/ok-oldking/ok-script-boilerplate'
            }
        },
    'screenshots_folder': "screenshots", #截图存放目录, 每次重新启动会清空目录
    'gui_title': 'ok-script-boilerplate',  # Optional
    'template_matching': {
        'coco_feature_json': os.path.join('assets', 'result.json'), #coco格式标记, 需要png图片, 在debug模式运行后, 会对进行切图仅保留被标记部分以减少图片大小
        'default_horizontal_variance': 0.002, #默认x偏移, 查找不传box的时候, 会根据coco坐标, match偏移box内的
        'default_vertical_variance': 0.002, #默认y偏移
        'default_threshold': 0.8, #默认threshold
    },
    'version': version, #版本
    'my_app': ['src.globals', 'Globals'], # 全局单例对象, 可以存放加载的模型, 使用og.my_app调用
    'onetime_tasks': [  # tasks to execute
        ["src.tasks.DailyTask", "DailyTask"],
        ["src.tasks.JiejiePersonTask", "JiejiePersonTask"],
        ["src.tasks.YuhunTask", "YuhunTask"],
        ["src.tasks.YulingTask", "YulingTask"],
        ["src.tasks.YeyuanhuoTask", "YeyuanhuoTask"],
        ["src.tasks.JuexingTask", "JuexingTask"],
        ["src.tasks.QilingTask", "QilingTask"],
        ["src.tasks.JiejieLiaoTask", "JiejieLiaoTask"],
    ],
    'trigger_tasks':[
        ["src.tasks.MyTriggerTask", "MyTriggerTask"],
    ]
}
