"""
计算的主入口
"""
import traceback
import gradio as gr
import pandas as pd
import json

from src.tool_func import logger, rune_json
from src.player_base_func import player_base_func
from src.equipment_func import equipment_func
from src.glyph_func import glyph_func, glyph_json
from src.rune_func import rune_func
from src.skin_func import skin_func
from src.surplus_func import surplus_func
from src.others_func import others_func
from src.percent_calculate import calculate_def_percent, \
    calculate_critical_percent, calculate_final_atk_percent
from src.dps_func import dps_func, def_func
from src.card_func import card_func

from gradio_ui.gr_warning_check import check_rune, check_glyph, check_equipment
from src.tool_func import add_dicts, job_info_dict, job_info_dict2, state_rate_json


def state_calculate(job,
                    player_state,
                    equipment_state,
                    glyph_state,
                    rune_state,
                    skin_state,
                    surplus_state,
                    others_state,
                    skill_state,
                    association_state,
                    card_state):
    """ 计算 """
    res_state_dict = {"力量": 0, "敏捷": 0, "智力": 0, "体质": 0,
                      "HP": 0, "MP": 0, "MP恢复": 0, "移速": 0,
                      "最小物攻": 0, "最大物攻": 0, "最小魔攻": 0, "最大魔攻": 0,
                      "防御": 0, "魔防": 0, "致命": 0, "最终": 0,
                      "防御百分比": 0, "魔防百分比": 0, "致命百分比": 0, "最终百分比": 0,
                      "火攻%": 0, "水攻%": 0, "光攻%": 0, "暗攻%": 0,
                      "火防%": 0, "水防%": 0, "光防%": 0, "暗防%": 0,
                      "眩晕": 0, "眩晕抵抗": 0, "硬直": 0, "硬直抵抗": 0,
                      "致命抵抗": 0, "额外伤害%": 0
                      }
    calculate_dict = {"力量": 0, "敏捷": 0, "智力": 0, "体质": 0,
                      "HP": 0, "MP": 0, "MP恢复": 0, "移速%": 0,
                      "HP%": 0, "MP%": 0, "MP恢复%": 0,
                      "最小物攻": 0, "最大物攻": 0, "最小魔攻": 0, "最大魔攻": 0,
                      "最小物攻%": 0, "最大物攻%": 0, "最小魔攻%": 0, "最大魔攻%": 0,
                      "物攻": 0, "魔攻": 0, "物攻%": 0, "魔攻%": 0,
                      "防御": 0, "魔防": 0, "致命": 0, "最终": 0,
                      "防御%": 0, "魔防%": 0, "致命%": 0, "致命面板%": 0,
                      "火攻%": 0, "水攻%": 0, "光攻%": 0, "暗攻%": 0,
                      "火防%": 0, "水防%": 0, "光防%": 0, "暗防%": 0,
                      "眩晕": 0, "眩晕抵抗": 0, "硬直": 0, "硬直抵抗": 0,
                      "眩晕%": 0, "眩晕抵抗%": 0, "硬直%": 0, "硬直抵抗%": 0,
                      "致命抵抗": 0, "致命抵抗%": 0, "额外伤害%": 0
                      }
    job_base = job_info_dict[job_info_dict2[job]]

    # 首先把基础属性汇总
    basic_state = add_dicts([player_state, equipment_state, glyph_state,
                             rune_state, skin_state, others_state, card_state])

    # 用于计算的dict
    calculate_dict = add_dicts([calculate_dict, basic_state])

    # 计算四维
    base_name_list = ["力量", "敏捷", "智力", "体质"]
    base_percent_name_list = ["力量%", "敏捷%", "智力%", "体质%"]
    for i in range(len(base_name_list)):
        skill_plus = 0
        if base_name_list[i] in skill_state:
            skill_plus = skill_state[base_name_list[i]]
        skill_rate = 1
        if base_percent_name_list[i] in skill_state:
            skill_rate = 1 + skill_state[base_percent_name_list[i]]
        basic_rate = 1
        if base_percent_name_list[i] in basic_state:
            basic_rate = 1 + basic_state[base_percent_name_list[i]]
        association_plus = 0
        if base_name_list[i] in association_state:
            association_plus = association_state[base_name_list[i]]
        association_rate = 1
        if base_percent_name_list[i] in association_state:
            association_rate = 1 + association_state[base_percent_name_list[i]]
        # 先乘装备之类的百分比，再乘技能给的百分比
        base_state_now = int(int(basic_state[base_name_list[i]] * basic_rate + skill_plus) * skill_rate)
        # 再计算公会buff
        base_state_now = int((base_state_now + association_plus) * association_rate)
        calculate_dict[base_name_list[i]] = base_state_now
        res_state_dict[base_name_list[i]] = base_state_now

    # 四维面板转换
    for base_name_now, val in state_rate_json[job_base].items():
        if base_name_now == "等级-MP恢复":
            calculate_dict["MP恢复"] += 50 * val
            continue
        for state_name_now, state_rate_now in val.items():
            calculate_dict[state_name_now] += int(calculate_dict[base_name_now] * state_rate_now)

    # 计算百分比加成
    calculate_dict["最小物攻"] = (calculate_dict["最小物攻"] + calculate_dict["物攻"]) * \
                             (1 + calculate_dict["最小物攻%"] + calculate_dict["物攻%"])
    calculate_dict["最大物攻"] = (calculate_dict["最大物攻"] + calculate_dict["物攻"]) * \
                             (1 + calculate_dict["最大物攻%"] + calculate_dict["物攻%"])
    calculate_dict["最小魔攻"] = (calculate_dict["最小魔攻"] + calculate_dict["魔攻"]) * \
                             (1 + calculate_dict["最小魔攻%"] + calculate_dict["魔攻%"])
    calculate_dict["最大魔攻"] = (calculate_dict["最大魔攻"] + calculate_dict["魔攻"]) * \
                             (1 + calculate_dict["最大魔攻%"] + calculate_dict["魔攻%"])
    for state_name_now in ["HP", "MP", "MP恢复", "防御", "魔防", "致命",
                           "眩晕", "眩晕抵抗", "硬直", "硬直抵抗", "致命抵抗"]:
        calculate_dict[state_name_now] = calculate_dict[state_name_now] * \
                                         (1 + calculate_dict[state_name_now + "%"])

    # 先加综合等级，再算技能buff加成
    calculate_dict = add_dicts([calculate_dict, surplus_state])

    # 最后一步算技能buff加成
    calculate_skill_dict = {"HP%": 0, "MP%": 0, "MP恢复%": 0,
                            "物攻": 0, "魔攻": 0, "物攻%": 0, "魔攻%": 0,
                            "致命": 0, "致命面板%": 0, "眩晕面板%": 0,
                            "光攻%": 0, "暗攻%": 0, "火攻%": 0, "水攻%": 0,
                            "力量转魔攻%": 0, "智力转物攻%": 0}
    calculate_skill_dict = add_dicts([calculate_skill_dict, skill_state])
    # 计算审判力量加成
    calculate_skill_dict["物攻"] += calculate_dict["智力"] * calculate_skill_dict["智力转物攻%"]
    calculate_skill_dict["魔攻"] += calculate_dict["力量"] * calculate_skill_dict["力量转魔攻%"]
    calculate_dict["最小物攻"] = (calculate_dict["最小物攻"] + calculate_skill_dict["物攻"]) * \
                             (1 + calculate_skill_dict["物攻%"])
    calculate_dict["最大物攻"] = (calculate_dict["最大物攻"] + calculate_skill_dict["物攻"]) * \
                             (1 + calculate_skill_dict["物攻%"])
    calculate_dict["最小魔攻"] = (calculate_dict["最小魔攻"] + calculate_skill_dict["魔攻"]) * \
                             (1 + calculate_skill_dict["魔攻%"])
    calculate_dict["最大魔攻"] = (calculate_dict["最大魔攻"] + calculate_skill_dict["魔攻"]) * \
                             (1 + calculate_skill_dict["魔攻%"])
    for state_name_now in ["HP", "MP", "MP恢复"]:
        calculate_dict[state_name_now] = calculate_dict[state_name_now] * \
                                         (1 + calculate_skill_dict[state_name_now + "%"])
    for state_name_now in ["致命", "致命面板%", "光攻%", "暗攻%", "火攻%", "水攻%"]:
        calculate_dict[state_name_now] += calculate_skill_dict[state_name_now]

    for key, val in res_state_dict.items():
        if key in calculate_dict:
            if "%" not in key:
                res_state_dict[key] = int(calculate_dict[key])
            else:
                res_state_dict[key] = calculate_dict[key]

    res_state_dict["防御百分比"] = calculate_def_percent(res_state_dict["防御"])
    res_state_dict["魔防百分比"] = calculate_def_percent(res_state_dict["魔防"])
    res_state_dict["致命百分比"] = min(calculate_critical_percent(res_state_dict["致命"]) + \
                                  calculate_dict["致命面板%"] * 100, 90)
    res_state_dict["最终百分比"] = calculate_final_atk_percent(res_state_dict["最终"])

    return res_state_dict


def dps_increase_calculate(job,
                           player_state,
                           equipment_state,
                           glyph_state,
                           rune_state,
                           skin_state,
                           surplus_state,
                           others_state,
                           skill_state,
                           association_state,
                           card_state,
                           final_state,
                           dps_list):
    """ 计算攻击属性收益 """
    glyph_plus_dict = {"最大物攻": "三属性物攻", "最大魔攻": "三属性魔攻", "致命": "三属性致命",
                       "力量": "三属性力量", "敏捷": "三属性敏捷", "智力": "三属性智力", "最终": "三属性最终"}
    rune_dict = {"物攻": "石板物攻", "魔攻": "石板魔攻", "致命": "石板致命",
                 "力量": "石板力量", "敏捷": "石板敏捷", "智力": "石板智力",
                 "最终": "石板最终"}

    ori_dps = dps_func(list(dps_list) + [final_state])

    res_dps_list = []

    for key, val in glyph_plus_dict.items():
        tmp_state = add_dicts([others_state, glyph_json["plus"]["50A"][key]])
        tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                          skin_state, surplus_state, tmp_state, skill_state, association_state,
                                          card_state,)
        dps_now = dps_func(list(dps_list) + [tmp_final_state])
        res_dps_list.append((round((dps_now - ori_dps) / ori_dps * 100, 2), val))

    for key, val in rune_dict.items():
        tmp_state = add_dicts([others_state, {key: max(rune_json["atk"][key])}])
        tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                          skin_state, surplus_state, tmp_state, skill_state, association_state,
                                          card_state,)
        dps_now = dps_func(list(dps_list) + [tmp_final_state])
        res_dps_list.append((round((dps_now - ori_dps) / ori_dps * 100, 2), val))

    # 输出格式规整
    # res_dps_text = f"您面对【{dps_list[-1]}】使用【{dps_list[1]}】属性【{dps_list[0]}】技能的战斗力竟然高达【{ori_dps}】! ! !"
    res_dps_text = f"您面对【{dps_list[-1]}】使用\n"
    for (atk_type1_now, atk_type2_now, atk_num1_now) in [(dps_list[0], dps_list[1], dps_list[2]),
                                                         (dps_list[5], dps_list[6], dps_list[7]),
                                                         (dps_list[10], dps_list[11], dps_list[12])]:
        if atk_type1_now != "无" and atk_num1_now > 0:
            res_dps_text += f"【{atk_type2_now}】属性【{atk_type1_now}】\n"
    res_dps_text += f"技能的战斗力竟然高达【{ori_dps}】! ! !"

    res_dps_dict_final = {"属性": [], "收益率": []}
    # res_dps_list.sort()
    for key, val in res_dps_list:
        if key != 0:
            res_dps_dict_final["属性"].append(val)
            res_dps_dict_final["收益率"].append(key)
    df = pd.DataFrame(res_dps_dict_final)

    return res_dps_text, df


def def_increase_calculate(job,
                           player_state,
                           equipment_state,
                           glyph_state,
                           rune_state,
                           skin_state,
                           surplus_state,
                           others_state,
                           skill_state,
                           association_state,
                           card_state,
                           final_state,
                           dps_list,
                           def_type="物防"):
    """ 计算防御属性收益 """
    if def_type == "物防":
        glyph_plus_dict = {"防御": "三属性防御", "体质": "三属性体质", "HP": "三属性HP"}
        rune_dict = {"防御": "石板防御", "体质": "石板体质", "HP": "石板HP"}
    else:
        glyph_plus_dict = {"魔防": "三属性魔防", "体质": "三属性体质", "HP": "三属性HP", "智力": "三属性智力"}
        rune_dict = {"魔防": "石板魔防", "体质": "石板体质", "HP": "石板HP", "智力": "石板智力"}

    ori_def = def_func(list(dps_list) + [final_state, def_type])

    res_def_list = []

    for key, val in glyph_plus_dict.items():
        tmp_state = add_dicts([others_state, glyph_json["plus"]["50A"][key]])
        tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                          skin_state, surplus_state, tmp_state, skill_state, association_state,
                                          card_state,)
        def_now = def_func(list(dps_list) + [tmp_final_state, def_type])
        res_def_list.append((round((def_now - ori_def) / ori_def * 100, 2), val))

    for key, val in rune_dict.items():
        for key2, val2 in rune_json.items():
            if key not in rune_json[key2]:
                continue
            tmp_state = add_dicts([others_state, {key: max(rune_json[key2][key])}])
            tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                              skin_state, surplus_state, tmp_state, skill_state, association_state,
                                              card_state,)
            def_now = def_func(list(dps_list) + [tmp_final_state, def_type])
            res_def_list.append((round((def_now - ori_def) / ori_def * 100, 2), val))

    # 输出格式规整
    res_def_text = f"您面对【{dps_list[-1]}】的【{def_type}】生存力足足有【{ori_def}】! ! !"
    res_def_dict_final = {"属性": [], "收益率": []}
    # res_dps_list.sort()
    for key, val in res_def_list:
        if key != 0:
            res_def_dict_final["属性"].append(val)
            res_def_dict_final["收益率"].append(key)
    df = pd.DataFrame(res_def_dict_final)
    # df_sorted = df.sort_values(by="收益率", ascending=False)

    return res_def_text, df


def get_out_format(job: str, input_dict: dict):
    text1 = f"职业: {job}\nHP: {input_dict['HP']}\nMP: {input_dict['MP']}\nMP恢复: {input_dict['MP恢复']}"
    text2 = f"力量: {input_dict['力量']}\n敏捷: {input_dict['敏捷']}\n" \
            f"智力: {input_dict['智力']}\n体质: {input_dict['体质']}"
    text3 = f"物攻: {input_dict['最小物攻']} ~ {input_dict['最大物攻']}\n" \
            f"魔攻: {input_dict['最小魔攻']} ~ {input_dict['最大魔攻']}\n" \
            f"防御: {input_dict['防御']}  ({input_dict['防御百分比']}%)\n" \
            f"魔防: {input_dict['魔防']}  ({input_dict['魔防百分比']}%)"
    text4 = f"致命: {input_dict['致命']}  ({input_dict['致命百分比']}%)\n" \
            f"眩晕: {input_dict['眩晕']}\n硬直: {input_dict['硬直']}\n" \
            f"最终: {input_dict['最终']}  ({input_dict['最终百分比']}%)"
    text5 = f"火攻: {round(input_dict['火攻%'] * 100, 2)}%\n" \
            f"水攻: {round(input_dict['水攻%'] * 100, 2)}%\n" \
            f"光攻: {round(input_dict['光攻%'] * 100, 2)}%\n" \
            f"暗攻: {round(input_dict['暗攻%'] * 100, 2)}%"
    text6 = f"火防: {round(input_dict['火防%'] * 100, 2)}%\n" \
            f"水防: {round(input_dict['水防%'] * 100, 2)}%\n" \
            f"光防: {round(input_dict['光防%'] * 100, 2)}%\n" \
            f"暗防: {round(input_dict['暗防%'] * 100, 2)}%"
    text7 = f"致命抵抗: {input_dict['致命抵抗']}\n眩晕抵抗: {input_dict['眩晕抵抗']}\n" \
            f"硬直抵抗: {input_dict['硬直抵抗']}"
    text8 = f"移速: {input_dict['移速']}"

    return [text1, text2, text3, text4, text5, text6, text7, text8]


def get_check_format(input_dict: dict):
    out_text = ""
    for key, val in input_dict.items():
        out_text += str(key) + ": " + str(val) + "\n"

    return out_text.strip()


def main_func(*args):
    """ 主入口 """

    def _error_return(err_msg: str):
        # 18 个输出占位, 与正常路径长度一致
        empty_blocks = [err_msg] + ["" for _ in range(7)]  # 面板8块
        dps_part = ["出错:" + err_msg, gr.update(value=None)]
        def_part = ["出错:" + err_msg, gr.update(value=None)]
        mdef_part = ["出错:" + err_msg, gr.update(value=None)]
        check_part = ["", "", "", ""]
        logger.info("输入(错误): " + str(args) + "; 错误: " + err_msg)
        return empty_blocks + dps_part + def_part + mdef_part + check_part

    # 1. 解析 metadata
    if not args or not isinstance(args[-1], str):
        return _error_return("缺少metadata")
    try:
        segment_lengths = json.loads(args[-1])
    except Exception:
        return _error_return("metadata解析失败")

    required_keys = ["equipment", "glyph_base", "glyph_plus", "rune",
                     "skin", "surplus", "other", "dps", "card_skill", "card"]
    if not all(k in segment_lengths for k in required_keys):
        return _error_return("metadata缺少必要字段")

    # 去掉 metadata 参数本体
    args = args[:-1]

    # 2. 根据长度切片
    pos = 0
    try:
        job_now = args[pos]; pos += 1
        equipment_list = list(args[pos: pos + segment_lengths["equipment"]]); pos += segment_lengths["equipment"]
        glyph_base_list = list(args[pos: pos + segment_lengths["glyph_base"]]); pos += segment_lengths["glyph_base"]
        glyph_plus_list = list(args[pos: pos + segment_lengths["glyph_plus"]]); pos += segment_lengths["glyph_plus"]
        rune_list = list(args[pos: pos + segment_lengths["rune"]]); pos += segment_lengths["rune"]
        skin_list = list(args[pos: pos + segment_lengths["skin"]]); pos += segment_lengths["skin"]
        surplus_list = list(args[pos: pos + segment_lengths["surplus"]]); pos += segment_lengths["surplus"]
        others_list = list(args[pos: pos + segment_lengths["other"]]); pos += segment_lengths["other"]
        dps_list = list(args[pos: pos + segment_lengths["dps"]]); pos += segment_lengths["dps"]
        card_skill_list = list(args[pos: pos + segment_lengths["card_skill"]]); pos += segment_lengths["card_skill"]
        card_list = list(args[pos: pos + segment_lengths["card"]]); pos += segment_lengths["card"]
    except Exception as e:
        return _error_return("切片失败:" + str(e))

    # 长度校验 (防止 UI 新增后 metadata 未同步或输入缺失)
    expected_total = 1 + sum(segment_lengths[k] for k in required_keys)
    if len(args) != expected_total:
        return _error_return(f"输入数量({len(args)})与metadata期望({expected_total})不符")

    # 3. 验证职业合法性
    if job_now in ["无", "请选择你的职业", "", None] or job_now not in job_info_dict2:
        return _error_return("职业未选择或非法")

    try:
        # 基础属性
        player_base_state = player_base_func(job_now)
        # 装备属性
        check_equipment(equipment_list)
        equipment_state = equipment_func(job_now, equipment_list)
        # 纹章属性
        glyph_input_combined = list(glyph_base_list) + list(glyph_plus_list)
        check_glyph(glyph_input_combined)
        glyph_state = glyph_func(glyph_input_combined)
        # 石板属性
        check_rune(rune_list)
        rune_state = rune_func(rune_list)
        # 时装属性
        skin_state = skin_func(skin_list)
        # 综合等级
        surplus_state = surplus_func(surplus_list)
        # 其他属性
        others_state, skill_state, association_state, collection_state = others_func(job_now, others_list)
        # 卡片属性
        card_state = card_func(list(card_skill_list) + list(card_list))
        # 面板最终属性
        final_state = state_calculate(job_now,
                                      player_base_state, equipment_state, glyph_state,
                                      rune_state, skin_state, surplus_state,
                                      others_state, skill_state, association_state, card_state)
        # 战斗力/防御收益
        dps_text, dps_increase_df = dps_increase_calculate(job_now,
                                                           player_base_state, equipment_state, glyph_state,
                                                           rune_state, skin_state, surplus_state,
                                                           others_state, skill_state, association_state,
                                                           card_state,
                                                           final_state, dps_list)
        def_text, def_increase_df = def_increase_calculate(job_now,
                                                           player_base_state, equipment_state, glyph_state,
                                                           rune_state, skin_state, surplus_state,
                                                           others_state, skill_state, association_state,
                                                           card_state,
                                                           final_state, dps_list, "物防")
        magic_def_text, magic_def_increase_df = def_increase_calculate(job_now,
                                                                       player_base_state, equipment_state, glyph_state,
                                                                       rune_state, skin_state, surplus_state,
                                                                       others_state, skill_state, association_state,
                                                                       card_state,
                                                                       final_state, dps_list, "魔防")
        out_text_list = get_out_format(job_now, final_state)
    except Exception:
        error_message = traceback.format_exc()
        print(error_message)
        return _error_return("计算异常")

    logger.info("输入(OK): job=" + str(job_now) + ", segments=" + json.dumps(segment_lengths, ensure_ascii=False))

    return out_text_list + \
           [dps_text, gr.update(value=dps_increase_df),
            def_text, gr.update(value=def_increase_df),
            magic_def_text, gr.update(value=magic_def_increase_df)] + \
           [get_check_format(glyph_state), get_check_format(card_state),
            get_check_format(rune_state), get_check_format(collection_state)]
