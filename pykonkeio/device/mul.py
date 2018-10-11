from .basemul import BaseMul

USB_COUNT = 2
SOCKET_COUNT = 3


class Mul(BaseMul):

    def __init__(self, ip):
        self.usb_status = ['close'] * USB_COUNT
        super().__init__(ip, 'relay')

    @property
    def socket_count(self):
        return SOCKET_COUNT

    def do(self, action, value=None):
        usb_device_id = action[-1:0]
        if usb_device_id.isnumeric() and 0 < int(usb_device_id) <= self.socket_count:
            usb_device_id = int(usb_device_id - 1)
        else:
            usb_device_id = False

        if action == 'get_usb_count':
            return USB_COUNT
        elif action == 'get_usb_status_all':
            return 'on' if all(status == 'open' for status in self.usb_status) else 'off'
        elif action[:-1] == 'get_usb_status' and usb_device_id:
            return 'on' if self.usb_status[usb_device_id] == 'open' else 'off'
        elif action == 'turn_on_usb' and usb_device_id:
            self.turn_on_usb(usb_device_id)
        elif action == 'turn_off_usb' and usb_device_id:
            self.turn_off_usb(usb_device_id)
        else:
            return super().do(action, value)

    """
        获取状态
        req: lan_phone%28-d9-8a-XX-XX-XX%XXXXXXXX%check%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open1,close2%uack
    """
    def update(self):
        super().update()

        for t, index in enumerate(self.send_message('check', 'usb').split(',')):
            self.usb_status[index] = t[:-1]

    """
        打开USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%openX%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%uack
    """
    def turn_on_usb(self, index):
        if self.usb_status[index] != 'open':
            self.send_message('open' + str(index + 1, 'usb'))
            self.usb_status[index] = 'open'

    """
        关闭USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%uack
    """
    def turn_off_usb(self, index):
        if self.usb_status[index] != 'close':
            self.send_message('close' + str(index + 1, 'usb'))
            self.usb_status[index] = 'close'
