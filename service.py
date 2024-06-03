import re

from types import FunctionType
from hoshino import Service
from hoshino.typing import CQEvent

from .Inquiry.module import Inquiry

sv = Service("红烧天堂数据查询")
blacklist = []

def help_doc(c):
    output = ''
    for [method_name, method] in c.__dict__.items():
        if type(method) == FunctionType and not method_name.startswith('_'):
            try:
                output += f'{method.__doc__}' + '\n'
            except:
                output += f'{method_name}' + '\n'
    return output.rstrip('\n')


inquiry = Inquiry('HBR_bak.db')
#inquiry = Inquiry()

@sv.on_prefix(('红烧查询'))
async def info_center(bot, ev: CQEvent):
    if ev.user_id not in blacklist:
        kws = re.split('\s+', ev.message.extract_plain_text().strip())
        len_kws = len(kws)
        msg = '输入参数格式有误，请重试。'
        if len_kws >= 2:
            msg = inquiry._wrap_msg(kws)
        elif len_kws == 1:
            r = False
            for pattern in ['指令', '帮助', 'help']:
                if re.search(pattern, kws[0]):
                    r = True
                    break
            if r:
                msg = help_doc(Inquiry)
        exceed_flag = False
        if len(msg) > 1000:
            msg = msg[:900]
            exceed_flag = True
        exceed_dict = {'\n': 0}
        for i, j in enumerate(msg):
            if j in exceed_dict:
                exceed_dict[j] = exceed_dict[j] + 1
            if exceed_dict['\n'] > 30:
                msg = msg[:i]
                msg = msg[:i]
                exceed_flag = True
                break
        if exceed_flag:
            msg = msg + "……\n（后面内容太多了，我就不继续往下念了……）"
        await bot.finish(ev, msg)
        
#if __name__ == "__main__":
    #print(help_doc(Inquiry))

    #i = Inquiry()
    #print(i._wrap_msg(['敌人', 'DeathSlug2nd','hoju']))
    #print(i.tag('六宇亚'))  # '月歌', 'kayamori', '可可怜', '四叶草'
    #print(i.tag_enemy('yuina'))  # , '幻影', '训练'
    #print(i.skill('月歌', '黎明'))  # ['一千子', 'attackupfire', 'param'], ['ADate', 'Skill51'], ['月歌', '星火', 'All']
    #print(i.skill_hit('千惠', '52'))
    #print(i.skill_accessory('防御下降')) # 'SP上升'
    #print(i.skill_name('isuzu')) # , '月歌', '白河', 'AbyssKnocker'，'Flathand'
    #print(i.passive('kura'))
    #print(i.enemy('Death','2ndomega','Hoju'))  # 'HardFlatHand2nd', 'value'
    #print(i.enemy_scoreattack('feeler','120'))
    #print(i.profile('rumi')) # , 'description'