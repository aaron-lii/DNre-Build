"""
用于保存配装和加载配装
"""
import os
import uuid
from datetime import datetime
import gradio as gr
import time

from src.tool_func import job_info_dict2, job_info_dict, player_base_state_json
from gradio_ui.gr_equipment import equipment_base_dict  # 用于加载时动态生成装备choices


load_data = []


def get_build_list():
    """ 默认保存列表 (新增 level) """
    res_list = [["level", sorted(player_base_state_json.keys(), key=lambda x: int(x))[-1]], ["job", "无"]]
    # 装备
    res_list += [["weapon1", "无"], ["weapon2", "无"], ["hat", "无"], ["cloths", "无"],
                 ["trousers", "无"], ["gloves", "无"], ["shoes", "无"]]
    # 后缀
    res_list += [["weapon1_suffix", "破坏"], ["weapon2_suffix", "铁壁"], ["hat_suffix", "铁壁"], ["cloths_suffix", "铁壁"],
                 ["trousers_suffix", "铁壁"], ["gloves_suffix", "铁壁"], ["shoes_suffix", "铁壁"]]
    # 强化
    res_list += [["weapon1_grade", 11], ["weapon2_grade", 11], ["hat_grade", 11], ["cloths_grade", 11],
                 ["trousers_grade", 11], ["gloves_grade", 11], ["shoes_grade", 11]]
    # 附魔
    res_list += [["weapon1_enchant", []], ["weapon2_enchant", []], ["hat_enchant", []], ["cloths_enchant", []],
                 ["trousers_enchant", []], ["gloves_enchant", []], ["shoes_enchant", []]]
    # 首饰及属性
    res_list += [["ring1", "无"], ["ring2", "无"], ["necklace", "无"], ["earrings", "无"],
                 ["ring1_state", "无"], ["ring2_state", "无"], ["necklace_state", "无"], ["earrings_state", "无"]]
    # 首饰附魔
    res_list += [["ring1_enchant", []], ["ring2_enchant", []], ["necklace_enchant", []], ["earrings_enchant", []]]
    # 纹章
    for i in range(11):
        res_list.append([f"glyph{i + 1}", "无"])
    # 纹章三属性
    for i in range(11):
        res_list.append([f"glyph{i + 1}_p", "无"])
    # 石板属性
    for i in range(4):
        for j in range(4):
            res_list.append([f"rune{i * 4 + j + 1}", "无"])
        for j in range(2):
            res_list.append([f"rune{16 + i * 2 + j + 1}", "无"])
    # 石板数值
    for i in range(4):
        for j in range(4):
            res_list.append([f"rune{i * 4 + j + 1}_p", "无"])
        for j in range(2):
            res_list.append([f"rune{16 + i * 2 + j + 1}_p", "无"])
    # 时装
    res_list += [["weapon1_skin", "无"], ["weapon2_skin", "无"],
                 ["wing_skin", "无"], ["tail_skin", "无"], ["printing_skin", "无"],
                 ["necklace_skin", "无"], ["earrings_skin", "无"], ["ring1_skin", "无"], ["ring2_skin", "无"]]
    # 综合等级
    for i in range(16):
        res_list.append([f"property{i + 1}_levle", 0])
    # 称号和收集
    res_list += [["appellation", "无"], ["skin_collections", 0]]
    # 被动技能
    for i in range(8):
        res_list.append([f"skill{i + 1}", 0])
    # 个人buff
    for i in range(4):
        res_list.append([f"personal_skill{i + 1}", 0])
    # 团队buff
    for i in range(12):
        res_list.append([f"team_skill{i + 1}", 0])
    # 公会buff
    for i in range(4):
        res_list.append([f"association_skill{i + 1}", 0])
    # 战力计算
    res_list += [["atk_type1", "物理"], ["atk_type2", "无"], ["atk_num1", 100], ["atk_num2", 0], ["glyph_plus1", 0],
                 ["atk_type3", "无"], ["atk_type4", "无"], ["atk_num3", 0], ["atk_num4", 0], ["glyph_plus3", 0],
                 ["atk_type5", "无"], ["atk_type6", "无"], ["atk_num5", 0], ["atk_num6", 0], ["glyph_plus5", 0],
                 ["target_boss", "地狱主教-石人胡知诺斯"]]

    for i in range(12):
        res_list.append([f"card_skill_{i + 1}", 0])
    for i in range(57):
        res_list.append([f"card_{i + 1}", "无"])

    return res_list


def save_options(*args):
    """ 保存配置文件 (首位新增level) """
    random_id = uuid.uuid4()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    # args[1] 才是 job (因为 args[0] 是 level)
    job_now = args[1]

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
    """ 加载配置文件 (兼容旧版: 无level字段) """
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
                    # 新版存档 (或兼容旧版缺少level/job)
                    for i in range(len(default_list)):
                        key = default_list[i][0]
                        if key in load_now:
                            load_data.append(load_now[key])
                        else:
                            load_data.append(default_list[i][1])
                else:
                    # 旧版列表格式 (首位是job), 无level
                    # 构造: level默认 + 原列表
                    load_data.append(default_list[0][1])  # level 默认
                    for i in range(len(default_list) - 1):
                        if i < len(load_now):
                            load_data.append(load_now[i])
                        else:
                            load_data.append(default_list[i + 1][1])
            except Exception as e:
                print(e)
                gr.Warning("加载配置文件出错")
    if len(load_data) == 0:
        raise gr.Error("加载配置文件出错")

    # 先根据存档内的job生成装备choices，避免第一次加载时报错
    res_val = []
    # job 索引为1 (因为0是level)
    job_val = load_data[1]
    # 装备索引 2-8
    equipment_indices = list(range(2, 9))
    if job_val != "无":
        try:
            mid_job = job_info_dict2[job_val]
            base_job = job_info_dict[mid_job]
            star_pre = "40S-海龙"
            part_order = ["主手", "副手", "头盔", "上装", "下装", "手套", "鞋子"]
            choice_lists = []
            for part in part_order:
                star_equipment_list = []
                for equipment_name in equipment_base_dict[base_job][part]:
                    if star_pre in equipment_name:
                        star_equipment_list += [equipment_name + "★", equipment_name + "★★", equipment_name + "★★★"]
                choice_lists.append(["无"] + sorted(star_equipment_list +
                                                 equipment_base_dict[mid_job][part] +
                                                 equipment_base_dict[base_job][part]))
        except Exception:
            choice_lists = [["无"]] * 7
    else:
        choice_lists = [["无"]] * 7

    # 构建输出 updates
    for i in range(len(load_data)):
        if i == 0:  # level
            # 等级下拉 choices 就是 player_base_state_json keys
            level_choices = ["请选择等级"] + sorted(player_base_state_json.keys(), key=lambda x: int(x))
            res_val.append(gr.update(value=load_data[i], choices=level_choices))
        elif i == 1:  # job
            res_val.append(gr.update(value=load_data[i]))
        elif i in equipment_indices:
            res_val.append(gr.update(value=load_data[i], choices=choice_lists[i - 2]))
        else:
            res_val.append(gr.update(value=load_data[i]))

    return res_val


def load_options2():
    """ 二次加载配置文件 """
    global load_data
    # 不等待的话gradio来不及更新
    time.sleep(1)

    return load_data
