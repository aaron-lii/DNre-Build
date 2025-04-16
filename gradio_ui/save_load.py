"""
用于保存配装和加载配装
"""
import os
import uuid
from datetime import datetime
import gradio as gr
import time


load_data = []


def get_build_list():
    """ 默认保存列表 """
    res_list = [["job", "无"],
                ["weapon1", "无"], ["weapon2", "无"], ["hat", "无"], ["cloths", "无"],
                ["trousers", "无"], ["gloves", "无"], ["shoes", "无"],
                ["weapon1_suffix", "破坏"], ["weapon2_suffix", "铁壁"], ["hat_suffix", "铁壁"], ["cloths_suffix", "铁壁"],
                ["trousers_suffix", "铁壁"], ["gloves_suffix", "铁壁"], ["shoes_suffix", "铁壁"],
                ["weapon1_grade", 11], ["weapon2_grade", 11], ["hat_grade", 11], ["cloths_grade", 11],
                ["trousers_grade", 11], ["gloves_grade", 11], ["shoes_grade", 11],
                ["weapon1_enchant", []], ["weapon2_enchant", []], ["hat_enchant", []], ["cloths_enchant", []],
                ["trousers_enchant", []], ["gloves_enchant", []], ["shoes_enchant", []],
                ["ring1", "无"], ["ring2", "无"], ["necklace", "无"], ["earrings", "无"],
                ["ring1_state", "无"], ["ring2_state", "无"], ["necklace_state", "无"], ["earrings_state", "无"],
                ["ring1_enchant", []], ["ring2_enchant", []], ["necklace_enchant", []], ["earrings_enchant", []],
                ["glyph1", "无"], ["glyph2", "无"], ["glyph3", "无"], ["glyph4", "无"],
                ["glyph5", "无"], ["glyph6", "无"], ["glyph7", "无"], ["glyph8", "无"],
                ["glyph9", "无"], ["glyph10", "无"], ["glyph11", "无"],
                ["glyph1_p", "无"], ["glyph2_p", "无"], ["glyph3_p", "无"], ["glyph4_p", "无"],
                ["glyph5_p", "无"], ["glyph6_p", "无"], ["glyph7_p", "无"], ["glyph8_p", "无"],
                ["glyph9_p", "无"], ["glyph10_p", "无"], ["glyph11_p", "无"],
                ["rune1", "无"], ["rune2", "无"], ["rune3", "无"], ["rune4", "无"],
                ["rune17", "无"], ["rune18", "无"],
                ["rune5", "无"], ["rune6", "无"], ["rune7", "无"], ["rune8", "无"],
                ["rune19", "无"], ["rune20", "无"],
                ["rune9", "无"], ["rune10", "无"], ["rune11", "无"], ["rune12", "无"],
                ["rune21", "无"], ["rune22", "无"],
                ["rune13", "无"], ["rune14", "无"], ["rune15", "无"], ["rune16", "无"],
                ["rune23", "无"], ["rune24", "无"],
                ["rune1_p", "无"], ["rune2_p", "无"], ["rune3_p", "无"], ["rune4_p", "无"],
                ["rune17_p", "无"], ["rune18_p", "无"],
                ["rune5_p", "无"], ["rune6_p", "无"], ["rune7_p", "无"], ["rune8_p", "无"],
                ["rune19_p", "无"], ["rune20_p", "无"],
                ["rune9_p", "无"], ["rune10_p", "无"], ["rune11_p", "无"], ["rune12_p", "无"],
                ["rune21_p", "无"], ["rune22_p", "无"],
                ["rune13_p", "无"], ["rune14_p", "无"], ["rune15_p", "无"], ["rune16_p", "无"],
                ["rune23_p", "无"], ["rune24_p", "无"],
                ["weapon1_skin", "无"], ["weapon2_skin", "无"],
                ["wing_skin", "无"], ["tail_skin", "无"], ["printing_skin", "无"],
                ["necklace_skin", "无"], ["earrings_skin", "无"], ["ring1_skin", "无"], ["ring2_skin", "无"],
                ["property1_levle", 0], ["property2_levle", 0], ["property3_levle", 0], ["property4_levle", 0],
                ["property5_levle", 0], ["property6_levle", 0], ["property7_levle", 0], ["property8_levle", 0],
                ["property9_levle", 0], ["property10_levle", 0], ["property11_levle", 0], ["property12_levle", 0],
                ["property13_levle", 0], ["property14_levle", 0], ["property15_levle", 0], ["property16_levle", 0],
                ["appellation", "无"], ["skin_collections", 0],
                ["skill1", 0], ["skill2", 0], ["skill3", 0], ["skill4", 0],
                ["skill5", 0], ["skill6", 0], ["skill7", 0], ["skill8", 0],
                ["personal_skill1", 0], ["personal_skill2", 0], ["personal_skill3", 0], ["personal_skill4", 0],
                ["team_skill1", 0], ["team_skill2", 0], ["team_skill3", 0], ["team_skill4", 0],
                ["team_skill5", 0], ["team_skill6", 0], ["team_skill7", 0], ["team_skill8", 0],
                ["association_skill1", 0], ["association_skill2", 0],
                ["association_skill3", 0], ["association_skill4", 0],
                ["atk_type1", "物理"], ["atk_type2", "无"], ["atk_num1", 100], ["atk_num2", 0],
                ["atk_type3", "无"], ["atk_type4", "无"], ["atk_num3", 0], ["atk_num4", 0],
                ["atk_type5", "无"], ["atk_type6", "无"], ["atk_num5", 0], ["atk_num6", 0],
                ["target_boss", "地狱主教-石人胡知诺斯"]
                ]

    return res_list


def save_options(*args):
    """ 保存配置文件 """
    random_id = uuid.uuid4()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    job_now = args[0]

    save_dir = os.path.join("dnre_saves", str(random_id))
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{job_now}{formatted_date}.txt")

    res_dict = {}
    default_list = get_build_list()
    for i in range(len(default_list)):
        res_dict[default_list[i][0]] = args[i]

    with open(save_path, "w", encoding='utf-8') as f_w:
        f_w.write(str(res_dict))

    return save_path


def load_options(input_file_path):
    """ 加载配置文件 """
    global load_data
    if not input_file_path:
        raise gr.Error("未上传配置文件")
    print(input_file_path)

    default_list = get_build_list()
    load_data = []
    with open(input_file_path, "r", encoding='utf-8') as f_r:
        for line in f_r.readlines():
            try:
                load_now = eval(line.strip())
                if isinstance(load_now, dict):
                    # 新版存档
                    for i in range(len(default_list)):
                        if default_list[i][0] in load_now:
                            load_data.append(load_now[default_list[i][0]])
                        else:
                            load_data.append(default_list[i][1])
                else:
                    # 兼容旧版存档
                    for i in range(len(default_list)):
                        if i < 63:
                            load_data.append(load_now[i])
                        else:
                            load_data.append(default_list[i][1])
            except Exception as e:
                print(e)
                gr.Warning("加载配置文件出错")
    if len(load_data) == 0:
        raise gr.Error("加载配置文件出错")

    res_val = []
    for i in range(len(load_data)):
        res_val.append(gr.update(value=load_data[i]))

    return res_val


def load_options2():
    """ 二次加载配置文件 """
    global load_data
    # 不等待的话gradio来不及更新
    time.sleep(1)

    return load_data

