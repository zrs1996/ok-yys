from ok import Logger
logger = Logger.get_logger(__name__)
from src.tasks.MyBaseTask import MyBaseTask

class TestTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试"
        self.default_config.update({
            '需要获取指定屏幕位置的颜色': True,
            'x': 0,
            'y': 0,
            '需要获取指定屏幕位置之后区域的文字识别': True,
        })

    def run(self):
        self.test()


    # 支持多个窗口 各种事件指定从该窗口获取

    def test(self):
        self.findOcr(match='')
        needCheckColor = self.config.get('需要获取指定屏幕位置的颜色')
        if needCheckColor:
            x1 = self.config.get('x')
            y1 = self.config.get('y')
            print(f'x1 {x1} y1 {y1}')
            self.checkColor(x1=x1,y1=y1)