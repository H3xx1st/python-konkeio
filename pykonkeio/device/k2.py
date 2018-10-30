from .basetoggle import BaseToggle


class K2(BaseToggle):

    def __init__(self, ip):
        self.light_status = 'close'
        self.usb_status = 'close'
        super().__init__(ip, 'relay')

    async def do(self, action, value=None):
        if action == 'get_usb_status':
            return 'on' if self.usb_status == 'open' else 'off'
        elif action == 'get_light_status':
            return 'on' if self.light_status == 'open' else 'off'
        elif action == 'get_power':
            return await self.get_power()
        elif action == 'turn_on_usb':
            await self.turn_on_usb()
        elif action == 'turn_off_usb':
            await self.turn_off_usb()
        elif action == 'turn_on_light':
            await self.turn_on_light()
        elif action == 'turn_off_light':
            await self.turn_off_light()
        else:
            return await super().do(action, value)

    async def update(self, **kwargs):
        await super().update(**kwargs)
        self.usb_status = await self.send_message('check', 'usb', **kwargs)
        self.light_status = await self.send_message('check', 'light', **kwargs)

    """
        打开USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%uack
    """
    async def turn_on_usb(self, **kwargs):
        if self.usb_status != 'open':
            await self.send_message('open', 'usb', **kwargs)
            self.usb_status = 'open'

    """
        关闭USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%uack
    """
    async def turn_off_usb(self, **kwargs):
        if self.usb_status != 'close':
            await self.send_message('close', 'usb', **kwargs)
            self.usb_status = 'close'

    """
        打开夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%lack
    """
    async def turn_on_light(self, **kwargs):
        if self.light_status != 'open':
            await self.send_message('open', 'light', **kwargs)
            self.light_status = 'open'

    """
        关闭夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%lack
    """
    async def turn_off_light(self, **kwargs):
        if self.light_status != 'close':
            await self.send_message('close', 'light', **kwargs)
            self.light_status = 'close'

    """
        获取实时功率
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%power
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%pack
    """
    async def get_power(self, **kwargs):
        res = await self.send_message('check', 'power', **kwargs)

        _, _, power = res.split('#')
        return power
