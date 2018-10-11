from .basebinary import BaseBinary
from .. import utils
from .. import error


class KBlub(BaseBinary):

    def __init__(self, ip):
        self.brightness = 0
        self.ct = 0
        self.mode = 0
        super().__init__(ip, 'kblub')

    def do(self, action, value=None):
        if action == 'get_brightness':
            return self.brightness
        elif action == 'get_color_temperature' or action == 'get_ct':
            return self.ct
        elif action == 'get_mode':
            return self.mode
        elif action == 'set_brightness':
            self.set_brightness(value)
        elif action == 'set_color_temperature' or action == 'set_ct':
            self.set_ct(value)
        else:
            return super().do(action, value)
    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open#x#x#x#x#1,x#1&#x#x#x#x#2,x#1&#x#x#x#x#3,x#1&#x#x#x#x#5,x#1%kbulb
    """
    def update(self):
        try:
            info = self.send_message('check').split('&')

            [self.status, modes] = info.split('#')
            [mode1, *_] = modes.split('&')
            [ct, lum, mode] = mode1.split(',')

            self.ct = int(ct)
            self.brightness = int(lum)
            self.mode = int(mode)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#lum#xxx%kbulb
    """
    def set_brightness(self, w):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        if self.brightness != int(w):
            self.set_mode(1)
            self.send_message('set#lum#%s' % w)
            self.brightness = int(w)

    """
        调整色温
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#ctp#xxx%kbulb
    """
    def set_ct(self, ct):
        try:
            utils.check_number(ct, 2700, 6500)
        except ValueError:
            raise error.IllegalValue('illegal color temperature')

        if self.ct != int(ct):
            self.set_mode(1)
            self.send_message('set#ctp#%s' % ct)
            self.ct = int(ct)

    """
        调整模式
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#mode#x%kbulb
    """
    def set_mode(self, mode):
        if self.mode != int(mode):
            self.send_message('set#mode#%s' % mode)
            self.mode = int(mode)
