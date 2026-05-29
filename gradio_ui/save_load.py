"""
用于保存配装和加载配装
"""
import os
import uuid
from datetime import datetime
import gradio as gr
import time

from src.tool_func import job_info_dict2, job_info_dict, player_base_state_json, rune_json
from src.tool_func import card_json
from gradio_ui.gr_equipment import equipment_base_dict  # 用于加载时动态生成装备choices
from gradio_ui.gr_skin import get_skin_data
from gradio_ui.gr_glyph import get_default_expedition_level_key, get_expedition_choice_lists, get_expedition_names, get_expedition_field_defs


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
    # 远征队纹章 (按 glyph2_json 顺序: 每种 = 等级 + base 合并后属性各一个下拉 + plus 下拉)
    try:
        default_level_key = get_default_expedition_level_key()
        for idx, glyph_name in enumerate(get_expedition_names(), start=1):
            field_defs = get_expedition_field_defs(glyph_name, default_level_key)
            for field_def in field_defs:
                if field_def["kind"] == "level":
                    res_list.append([f"expedition_{idx}_level", default_level_key])
                elif field_def["kind"] == "plus":
                    res_list.append([f"expedition_{idx}_plus", "无"])
                else:
                    res_list.append([f"expedition_{idx}_{field_def['label']}", "无"])
    except Exception:
        for i in range(4):
            res_list.append([f"expedition_{i+1}_level", "默认"])
        for i in range(11):
            res_list.append([f"expedition_base_{i + 1}", "无"])
        for i in range(4):
            res_list.append([f"expedition_{i + 1}_plus", "无"])
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
    # 源铸石板
    res_list += [["core_rune_attr", "无"], ["core_rune_ratio", "无"],
                 ["core_rune_coeff", "无"], ["core_rune_enhance", "0"]]
    # 新增: 四个石板板级别等级 (顺序紧随石板数值，计算不使用) - 默认取 rune.json 最低等级
    try:
        if isinstance(rune_json, dict) and rune_json:
            default_rune_level = sorted(rune_json.keys(), key=lambda x: int(x))[0]
        else:
            default_rune_level = "50"
    except Exception:
        default_rune_level = "50"
    res_list += [["rune_board_level1", default_rune_level],
                 ["rune_board_level2", default_rune_level],
                 ["rune_board_level3", default_rune_level],
                 ["rune_board_level4", default_rune_level]]
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
    for i in range(16):
        res_list.append([f"team_skill{i + 1}", 0])
    # 公会buff
    for i in range(4):
        res_list.append([f"association_skill{i + 1}", 0])
    # 战力计算
    res_list += [["atk_type1", "物理"], ["atk_type2", "无"], ["atk_num1", 100], ["atk_num2", 0], ["glyph_plus1", 0],
                 ["atk_type3", "无"], ["atk_type4", "无"], ["atk_num3", 0], ["atk_num4", 0], ["glyph_plus3", 0],
                 ["atk_type5", "无"], ["atk_type6", "无"], ["atk_num5", 0], ["atk_num6", 0], ["glyph_plus5", 0],
                 ["target_boss", "70试炼地狱-新月守护者佩尔守卫者"],
                 ["analysis_mode", "单槽替换"], ["replace_slot", "石板词条"]]

    for i in range(12):
        res_list.append([f"card_skill_{i + 1}", 0])
    # 动态卡片数量
    card_total = len(card_json.keys()) if isinstance(card_json, dict) else 0
    for i in range(card_total):
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
                    # 新版存档 (或兼容旧版缺少level/job/expedition) -> 逐键填充
                    for i in range(len(default_list)):
                        key = default_list[i][0]
                        if key in load_now:
                            load_data.append(load_now[key])
                        else:
                            load_data.append(default_list[i][1])
                elif isinstance(load_now, list):
                    # 旧的列表格式 (无 level, 也无 expedition) -> 重建映射
                    # 1) 构造旧键顺序: 默认列表去掉 level 与 expedition_*
                    old_keys = [k for (k, _v) in default_list if k != "level" and not k.startswith("expedition_")]
                    # 2) 先构造一个键->值映射 dict, 用默认值填充
                    tmp_map = {k: v for (k, v) in default_list}
                    # 3) 将旧列表的第 i 项赋值给 old_keys[i]
                    for i_val, val in enumerate(load_now):
                        if i_val < len(old_keys):
                            tmp_map[old_keys[i_val]] = val
                    # 4) 组装新的顺序输出: level 用默认, expedition_* 用默认
                    for (k, v_default) in default_list:
                        if k == "level":
                            load_data.append(v_default)  # 老存档无 level, 用默认最高等级
                        else:
                            load_data.append(tmp_map.get(k, v_default))
                else:
                    gr.Warning("未知的存档数据格式")
            except Exception as e:
                print(e)
                gr.Warning("加载配置文件出错")
    if len(load_data) == 0:
        raise gr.Error("加载配置文件出错")

    # 先根据存档内的job生成装备choices，避免第一次加载时报错
    res_val = []
    expedition_names = get_expedition_names()
    expedition_level_values = []
    expedition_level_idx = 0
    for key, value in zip([item[0] for item in default_list], load_data):
        if key.startswith("expedition_") and key.endswith("_level"):
            expedition_level_values.append(value)
            expedition_level_idx += 1
    if not expedition_level_values:
        expedition_level_values = [get_default_expedition_level_key()] * len(expedition_names)
    expedition_choice_lists = get_expedition_choice_lists(expedition_level_values)
    expedition_choice_index = 0
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
                base_part_equipment = equipment_base_dict.get(base_job, {}).get(part, [])
                mid_part_equipment = equipment_base_dict.get(mid_job, {}).get(part, [])
                for equipment_name in base_part_equipment:
                    if star_pre in equipment_name:
                        star_equipment_list += [equipment_name + "★", equipment_name + "★★", equipment_name + "★★★"]
                choice_lists.append(["无"] + sorted(star_equipment_list +
                                                 mid_part_equipment +
                                                 base_part_equipment))
            skin_choice_lists = get_skin_data(job_val)
        except Exception:
            choice_lists = [["无"]] * 7
            skin_choice_lists = [["无"], ["无"]]
    else:
        choice_lists = [["无"]] * 7
        skin_choice_lists = [["无"], ["无"]]

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
        elif default_list[i][0] == "weapon1_skin":
            value_now = load_data[i] if load_data[i] in skin_choice_lists[0] else "无"
            res_val.append(gr.update(value=value_now, choices=skin_choice_lists[0]))
        elif default_list[i][0] == "weapon2_skin":
            value_now = load_data[i] if load_data[i] in skin_choice_lists[1] else "无"
            res_val.append(gr.update(value=value_now, choices=skin_choice_lists[1]))
        elif default_list[i][0].startswith("expedition_"):
            if expedition_choice_index < len(expedition_choice_lists):
                choices_now = expedition_choice_lists[expedition_choice_index]
                expedition_choice_index += 1
            else:
                choices_now = ["无"]
            value_now = load_data[i] if load_data[i] in choices_now else "无"
            if default_list[i][0].endswith("_level") and "无" not in choices_now:
                value_now = load_data[i] if load_data[i] in choices_now else choices_now[0]
            res_val.append(gr.update(value=value_now, choices=choices_now))
        else:
            res_val.append(gr.update(value=load_data[i]))

    return res_val


def load_options2():
    """ 二次加载配置文件 """
    global load_data
    # 不等待的话gradio来不及更新
    time.sleep(2)

    return load_data
