from nonebot import require
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

from nonebot import on_command
from nonebot import on_message
from nonebot import on_notice
from nonebot import on_startswith

from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.exception import MatcherException
import os.path

from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, Event
from nonebot.typing import T_State

#require("requests")
from pip._vendor import requests
# from nonebot.drivers import aiohttp
import asyncio

import zipfile
from zipfile import BadZipFile

import os
import zipfile
import aiohttp
import asyncio

#[HBR]
import re
from types import FunctionType

from .Inquiry.module import Inquiry

#HBR2
import time
import pandas as pd
from typing import List

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_hbr_nanase",
    description="A plugin for Heaven Burns Red",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


current_directory = os.path.dirname(os.path.abspath(__file__))
stat_directory = os.path.join(current_directory, 'stat')
reply_directory = os.path.join(current_directory, 'replies')
csv_path = os.path.join(current_directory, 'main.csv')


async def download_file(session, url, filename):
    print(f'正在下载 {url} 到 {filename}')
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f'文件已下载并保存为 {filename}')
        else:
            print(f'下载失败，HTTP 状态码：{response.status}')
            return False
    return True

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"解压完成到 {extract_to}")

def check_files(directory):
    """List files in directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"Found file: {file}")
        for dir in dirs:
            print(f"Found directory: {dir}")

def load_reply(file_path):
    reply_path = os.path.join(reply_directory, file_path)

    fileTemp = open(reply_path, mode='r', buffering=-1, encoding="utf-8")
    result = fileTemp.read()
    fileTemp.close()
    return result

#HBR

sv = on_command("红烧数据查询", aliases={"hbr", "红烧查", "红茶"}, priority=10, block=False)
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



@sv.handle()
async def info_center(bot: Bot, ev: Event, state: T_State):
    if ev.user_id not in blacklist:
        kws = re.split('\s+', ev.message.extract_plain_text().strip())
        #remove the first element of kws if it exists
        if len(kws) > 0:
            kws.pop(0)
        print(kws)
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

        print(msg)
        await sv.finish(msg)
        
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

def node_custom(
    user_id: int, name: str, time: int, content: MessageSegment
) -> "MessageSegment":
    return MessageSegment(
        type="node",
        data={"uin": str(user_id), "name": name, "content": content, "time": time},
    )

quickList = on_command("传说", aliases={"ppx"}, priority=10, block=False)
@quickList.handle()
async def _(bot: Bot, event: Event):
    content_list = findChara("月歌")

    message_list: List[MessageSegment] = list()
    offset = 1
    for res in content_list:
        message_list.append(
            node_custom(
                content=res,
                user_id=3061694812,
                name="七濑七海",
                time=str(int(time.time())),
            )
        )
        offset += 1
    print("HAH啊")
    await bot.send_group_forward_msg(group_id=event.group_id, messages=message_list)
    await sv.finish("HAHA")

# 读取CSV文件
df = pd.read_csv(os.path.join(current_directory, 'csv_files/MiddleSkillList.csv'))

# 选择感兴趣的列
columns_of_interest = ['LabelName', 'TargetType', 'HitCount',"CharacterNamezhTW","SkillNamezhTW","InfozhTW","CardNamezhTW"]

# 过滤出所需的列
filtered_df = df[columns_of_interest]

# 打印过滤后的数据
# print(filtered_df)

# 保存过滤后的数据到新的CSV文件
# filtered_df.to_csv('filtered_skills.csv', index=False)

def findChara(chara_name):
    result = {}
    for index, row in df.iterrows():
        if row['CharacterNamezhTW'] == chara_name:
            #add printSkill(row) to result list
            result.append(printSkill(row))

    return result

def appendAttr(data,str,totalWeight,isFirst,key,name):
    if data[key] > 0:
        if not isFirst:
            str += "+"
        else:
            isFirst = True
        percentage = data[key] / totalWeight * 100
        str += f"{percentage:.0f}%{name}"
    return str

def format_float(value):
    try:
        return "{:.2f}".format(float(value))
    except ValueError:
        return value

def printSkill(data):
    result = ""
    if data["SkillType"] == "AttackNormal":
        return

    result +=(f"{data['CardNamezhTW']}【{data['SkillNamezhTW']}】 {data['InfozhTW']}")
    if data["HitCount"] > 0 :
        result +=(f"{data['HitCount']}段")

    
    totalWeight = data["RefParamPower"] + data["RefParamWisdom"] + data["RefParamDexterity"] + data["RefParamSpirit"] + data["RefParamLuck"] + data["RefParamToughness"]
    if totalWeight > 0:
        str = ""
        isFirst = True

        str = appendAttr(data,str,totalWeight,isFirst,"RefParamPower","力")
        str = appendAttr(data,str,totalWeight,isFirst,"RefParamWisdom","智")
        str = appendAttr(data,str,totalWeight,isFirst,"RefParamDexterity","敏")
        str = appendAttr(data,str,totalWeight,isFirst,"RefParamSpirit","精")
        str = appendAttr(data,str,totalWeight,isFirst,"RefParamLuck","运")
        str = appendAttr(data,str,totalWeight,isFirst,"RefParamToughness","体")

    if data["MaxPower"] > 0 :
        if data["SkillType"] in {"AttackNormal",  "AttackSkill", "AttackDp", "AttackDpSkill", "HealDp", "ReviveDp", "AttackByOwnDpRate","Funnel","DamageRateChangeAttackSkill"}:
            result +=(f"{data['Power']:.0f}~{data['MaxPower']:.0f}，需要{str}≥{data['RefParamDiffForMax']}")
        elif data["SkillType"] in {"SuperBreak"}:
            result +=(f"{data['Power']:.0f}%~{data['MaxPower']:.0f}%，需要{str}≥{data['RefParamDiffForMax']}")
        else:
            result +=(f"{data['Power']*100:.0f}%~{data['MaxPower']*100:.0f}%，需要{str}≥{data['RefParamDiffForMax']}")

    if data["TargetType"] == "All":
        result +=("（对敌全体）")

    result +=("")
    return result

# async def create_record(bot: Bot, event: GroupMessageEvent, target_id):
#     message = Message()
#     if event.reply:
#         message.append(MessageSegment.reply(event.reply.message_id))
#     for segment in event.message:
#         if segment.type == "at":
#             card = get_member_name(
#                 await bot.get_group_member_info(
#                     group_id=event.group_id, user_id=int(target_id)
#                 )
#             )
#             message.append(
#                 f"@{MessageSegment.text(card)}"
#                 if segment.data["qq"] != "all"
#                 else "@全体成员"
#             )
#             continue
#         message.append(segment)

#     MainTable.create(
#         operator_id=event.user_id,
#         operator_name=event.sender.card or event.sender.nickname,
#         target_id=target_id,
#         group_id=event.group_id,
#         time=str(int(time.time())),
#         message=message,
#         message_id=event.message_id,
#     )