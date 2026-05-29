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
from src.percent_calculate import calculate_defense_percent, \
    calculate_critical_percent, calculate_critical_damage_percent, calculate_final_atk_percent
from src.dps_func import dps_func, def_func
from src.card_func import card_func

from gradio_ui.gr_warning_check import check_rune, check_glyph, check_equipment, check_level
from src.tool_func import add_dicts, job_info_dict, job_info_dict2, state_rate_json, load_json

core_rune_json = load_json("core_rune")


def _glyph_level_key(player_level: str):
    """将当前人物等级映射到可用的纹章档位键。"""
    try:
        level_num = int(float(player_level))
    except Exception:
        level_num = 60

    available = []
    if isinstance(glyph_json, dict):
        plus_dict = glyph_json.get("plus", {})
        if isinstance(plus_dict, dict):
            for key in plus_dict.keys():
                try:
                    available.append((int(str(key).rstrip("A")), key))
                except Exception:
                    continue
    if not available:
        return "60A"

    available.sort()
    for num, key in reversed(available):
        if level_num >= num:
            return key
    return available[0][1]


def _rune_max_value(stat_name: str):
    """适配新版 rune_json 结构: level -> {atk:{}, def:{}} ; 返回指定属性的最大可能值(所有等级所有分类)."""
    max_v = 0
    try:
        if isinstance(rune_json, dict):
            for _lvl, cat_dict in rune_json.items():
                if not isinstance(cat_dict, dict):
                    continue
                for cat in ["atk", "def"]:
                    sub = cat_dict.get(cat, {})
                    if isinstance(sub, dict) and stat_name in sub:
                        vals = sub[stat_name]
                        if isinstance(vals, list) and vals:
                            mv = max(vals)
                            if mv > max_v:
                                max_v = mv
    except Exception:
        pass
    return max_v


def _split_dps_analysis_inputs(dps_list):
    """拆分战斗配置与收益分析配置。"""
    combat_list = list(dps_list[:16])
    analysis_mode = dps_list[16] if len(dps_list) > 16 else "单槽替换"
    replace_slot = dps_list[17] if len(dps_list) > 17 else "石板词条"
    return combat_list, analysis_mode, replace_slot


def _build_rune_slot_defs(rune_list, rune_board_levels, rune_type):
    """构建指定类型石板词条定义。"""
    if rune_type == "atk":
        board_indices = [0, 1]
        base_board_no = 1
    else:
        board_indices = [2, 3]
        base_board_no = 1

    res = []
    for offset, board_index in enumerate(board_indices):
        board_level = str(rune_board_levels[board_index]) if board_index < len(rune_board_levels) else "50"
        start = board_index * 6
        for slot_in_board in range(6):
            slot_index = start + slot_in_board
            rune_name = rune_list[slot_index] if slot_index < len(rune_list) else "无"
            rune_value = rune_list[24 + slot_index] if 24 + slot_index < len(rune_list) else "无"
            res.append({
                "slot_index": slot_index,
                "board_index": board_index,
                "board_no": base_board_no + offset,
                "slot_no": slot_in_board + 1,
                "level": board_level,
                "name": rune_name,
                "value": rune_value,
                "rune_type": rune_type,
            })
    return res


def _get_rune_value_tier(level, rune_type, rune_name, raw_value):
    """根据当前选中的石板属性值返回对应档位。"""
    try:
        values = rune_json[str(level)][rune_type][rune_name]
    except Exception:
        return None, None
    if not isinstance(values, list) or not values:
        return None, None

    try:
        value_num = int(float(raw_value))
    except Exception:
        return None, None

    if value_num in values:
        idx = values.index(value_num)
    else:
        idx = min(range(len(values)), key=lambda i: abs(values[i] - value_num))
    return idx, values


def _replace_rune_slot(rune_list, slot_index, new_name, new_value):
    """替换单个石板词条。"""
    tmp_rune_list = list(rune_list)
    tmp_rune_list[slot_index] = new_name
    tmp_rune_list[24 + slot_index] = str(new_value) if new_name not in ["无", "", None] else "无"
    return tmp_rune_list


def _describe_rune_slot(slot_info):
    if not slot_info:
        return "无"
    rune_type_text = "攻击石板" if slot_info["rune_type"] == "atk" else "防御石板"
    return (f"{rune_type_text}{slot_info['board_no']} 词条{slot_info['slot_no']} "
            f"[{slot_info['level']}级 {slot_info['name']} {slot_info['value']}]")


def _build_glyph_plus_slot_defs(glyph_names_list, glyph_p_names_list):
    """构建普通三属性纹章槽位定义。"""
    res = []
    for idx, (glyph_name, plus_name) in enumerate(zip(glyph_names_list, glyph_p_names_list)):
        if glyph_name in ["无", "", None]:
            continue
        try:
            level_key, base_name = str(glyph_name).split("-", 1)
        except Exception:
            continue
        res.append({
            "slot_index": idx,
            "level": level_key,
            "base_name": base_name,
            "plus_name": plus_name,
        })
    return res


def _replace_glyph_plus_slot(glyph_plus_list, slot_index, new_plus_name):
    tmp_glyph_plus_list = list(glyph_plus_list)
    tmp_glyph_plus_list[slot_index] = new_plus_name
    return tmp_glyph_plus_list


def _describe_glyph_slot(slot_info):
    if not slot_info:
        return "无"
    return f"纹章{slot_info['slot_index'] + 1} [{slot_info['level']}级 {slot_info['base_name']} / {slot_info['plus_name']}]"


def _recalculate_glyph_final_state(job,
                                   player_state,
                                   equipment_state,
                                   glyph_names_list,
                                   temp_glyph_plus_list,
                                   rune_state,
                                   skin_state,
                                   surplus_state,
                                   others_state,
                                   skill_state,
                                   association_state,
                                   card_state,
                                   expedition_part,
                                   player_level,
                                   core_rune_info):
    temp_glyph_state = glyph_func(list(glyph_names_list) + list(temp_glyph_plus_list) + list(expedition_part), player_level=player_level)
    return state_calculate(job, player_state, equipment_state, temp_glyph_state, rune_state,
                           skin_state, surplus_state, others_state, skill_state, association_state,
                           card_state, player_level=player_level, core_rune_info=core_rune_info)


def _find_least_valuable_glyph_slot(job,
                                    player_state,
                                    equipment_state,
                                    glyph_names_list,
                                    glyph_p_names_list,
                                    expedition_part,
                                    rune_state,
                                    skin_state,
                                    surplus_state,
                                    others_state,
                                    skill_state,
                                    association_state,
                                    card_state,
                                    player_level,
                                    core_rune_info,
                                    score_func,
                                    base_score):
    """找到当前收益最低的已装备三属性纹章槽位。"""
    best_slot = None
    best_loss = None
    for slot_info in _build_glyph_plus_slot_defs(glyph_names_list, glyph_p_names_list):
        if slot_info["plus_name"] in ["无", "", None]:
            continue
        temp_glyph_plus_list = _replace_glyph_plus_slot(glyph_p_names_list, slot_info["slot_index"], "无")
        temp_final_state = _recalculate_glyph_final_state(job, player_state, equipment_state, glyph_names_list,
                                                          temp_glyph_plus_list, rune_state, skin_state, surplus_state,
                                                          others_state, skill_state, association_state, card_state,
                                                          expedition_part, player_level, core_rune_info)
        score_now = score_func(temp_final_state)
        loss = base_score - score_now
        if best_loss is None or loss < best_loss:
            best_slot = slot_info
            best_loss = loss
    return best_slot, best_loss


def _get_glyph_replacement_results(job,
                                   player_state,
                                   equipment_state,
                                   glyph_names_list,
                                   glyph_p_names_list,
                                   expedition_part,
                                   rune_state,
                                   skin_state,
                                   surplus_state,
                                   others_state,
                                   skill_state,
                                   association_state,
                                   card_state,
                                   player_level,
                                   core_rune_info,
                                   score_func,
                                   base_score,
                                   glyph_candidates):
    """计算三属性纹章单槽替换收益。"""
    target_slot, _ = _find_least_valuable_glyph_slot(job, player_state, equipment_state, glyph_names_list,
                                                     glyph_p_names_list, expedition_part, rune_state, skin_state,
                                                     surplus_state, others_state, skill_state, association_state,
                                                     card_state, player_level, core_rune_info, score_func, base_score)
    if not target_slot:
        return [], None

    target_level = target_slot["level"]
    if target_level not in glyph_json.get("plus", {}):
        return [], target_slot

    res_list = []
    for stat_name, label in glyph_candidates.items():
        if stat_name not in glyph_json["plus"][target_level]:
            continue
        temp_glyph_plus_list = _replace_glyph_plus_slot(glyph_p_names_list, target_slot["slot_index"], stat_name)
        temp_final_state = _recalculate_glyph_final_state(job, player_state, equipment_state, glyph_names_list,
                                                          temp_glyph_plus_list, rune_state, skin_state, surplus_state,
                                                          others_state, skill_state, association_state, card_state,
                                                          expedition_part, player_level, core_rune_info)
        score_now = score_func(temp_final_state)
        increase = round((score_now - base_score) / base_score * 100, 2)
        if increase != 0:
            res_list.append((increase, label))
    return res_list, target_slot


def _recalculate_final_state(job,
                             player_state,
                             equipment_state,
                             glyph_state,
                             temp_rune_list,
                             skin_state,
                             surplus_state,
                             others_state,
                             skill_state,
                             association_state,
                             card_state,
                             player_level,
                             core_rune_info):
    temp_rune_state = rune_func(temp_rune_list)
    return state_calculate(job, player_state, equipment_state, glyph_state, temp_rune_state,
                           skin_state, surplus_state, others_state, skill_state, association_state,
                           card_state, player_level=player_level, core_rune_info=core_rune_info)


def _find_least_valuable_rune_slot(job,
                                   player_state,
                                   equipment_state,
                                   glyph_state,
                                   rune_list,
                                   rune_board_levels,
                                   skin_state,
                                   surplus_state,
                                   others_state,
                                   skill_state,
                                   association_state,
                                   card_state,
                                   player_level,
                                   core_rune_info,
                                   score_func,
                                   base_score,
                                   rune_type):
    """找到当前收益最低的已装备石板词条。"""
    best_slot = None
    best_loss = None
    for slot_info in _build_rune_slot_defs(rune_list, rune_board_levels, rune_type):
        if slot_info["name"] in ["无", "", None] or slot_info["value"] in ["无", "", None]:
            continue
        temp_rune_list = _replace_rune_slot(rune_list, slot_info["slot_index"], "无", "无")
        temp_final_state = _recalculate_final_state(job, player_state, equipment_state, glyph_state, temp_rune_list,
                                                    skin_state, surplus_state, others_state, skill_state,
                                                    association_state, card_state, player_level, core_rune_info)
        score_now = score_func(temp_final_state)
        loss = base_score - score_now
        if best_loss is None or loss < best_loss:
            best_slot = slot_info
            best_loss = loss
    return best_slot, best_loss


def _get_rune_replacement_results(job,
                                  player_state,
                                  equipment_state,
                                  glyph_state,
                                  rune_list,
                                  rune_board_levels,
                                  skin_state,
                                  surplus_state,
                                  others_state,
                                  skill_state,
                                  association_state,
                                  card_state,
                                  player_level,
                                  core_rune_info,
                                  score_func,
                                  base_score,
                                  rune_candidates,
                                  rune_type):
    """计算石板单槽替换收益。"""
    target_slot, _ = _find_least_valuable_rune_slot(job, player_state, equipment_state, glyph_state, rune_list,
                                                    rune_board_levels, skin_state, surplus_state, others_state,
                                                    skill_state, association_state, card_state, player_level,
                                                    core_rune_info, score_func, base_score, rune_type)
    if not target_slot:
        return [], None

    tier_idx, current_values = _get_rune_value_tier(target_slot["level"], rune_type, target_slot["name"], target_slot["value"])
    if tier_idx is None or current_values is None:
        return [], target_slot

    res_list = []
    for stat_name, label in rune_candidates.items():
        try:
            candidate_values = rune_json[str(target_slot["level"])][rune_type][stat_name]
        except Exception:
            continue
        if not isinstance(candidate_values, list) or not candidate_values:
            continue
        candidate_idx = min(tier_idx, len(candidate_values) - 1)
        candidate_value = candidate_values[candidate_idx]
        temp_rune_list = _replace_rune_slot(rune_list, target_slot["slot_index"], stat_name, candidate_value)
        temp_final_state = _recalculate_final_state(job, player_state, equipment_state, glyph_state, temp_rune_list,
                                                    skin_state, surplus_state, others_state, skill_state,
                                                    association_state, card_state, player_level, core_rune_info)
        score_now = score_func(temp_final_state)
        increase = round((score_now - base_score) / base_score * 100, 2)
        if increase != 0:
            res_list.append((increase, label))
    return res_list, target_slot


def _parse_core_rune_value(raw_val):
    """解析源铸石板下拉值，兼容 `等级 | 数值` 格式。返回(level_index, value)。"""
    if raw_val in [None, "", "无"]:
        return None, None
    try:
        text = str(raw_val).strip()
        level_index = None
        if "|" in text:
            level_text, text = text.split("|", 1)
            text = text.strip()
            level_index = int(float(level_text.strip())) - 1
        return level_index, float(text)
    except Exception:
        return None, None


def _extract_core_rune_info(rune_list):
    """从 rune_list 提取源铸石板配置。"""
    if len(rune_list) < 52:
        return None
    attr = rune_list[48]
    ratio_level_index, ratio = _parse_core_rune_value(rune_list[49])
    _coeff_level_index, coeff = _parse_core_rune_value(rune_list[50])
    if attr in [None, "", "无"] or ratio is None or coeff is None:
        return None
    if "→" not in str(attr):
        return None
    src, dst = str(attr).split("→", 1)
    src = src.strip()
    dst = dst.strip()
    if src == "" or dst == "":
        return None
    max_deduct = None
    try:
        attr_data = core_rune_json.get(str(attr), {}) if isinstance(core_rune_json, dict) else {}
        max_deduct_list = attr_data.get("最大扣除值", []) if isinstance(attr_data, dict) else []
        if isinstance(max_deduct_list, list) and max_deduct_list:
            if ratio_level_index is None or ratio_level_index < 0 or ratio_level_index >= len(max_deduct_list):
                ratio_level_index = 0
            max_deduct = float(max_deduct_list[ratio_level_index])
    except Exception:
        max_deduct = None
    return {
        "source": src,
        "target": dst,
        "ratio": ratio,
        "coefficient": coeff,
        "max_deduct": max_deduct,
    }


def _apply_core_rune_convert(calculate_dict, core_rune_info):
    """应用源铸石板转换：减源属性，加目标属性。"""
    if not core_rune_info:
        return

    source = core_rune_info["source"]
    target = core_rune_info["target"]
    ratio = core_rune_info["ratio"]
    coefficient = core_rune_info["coefficient"]
    max_deduct = core_rune_info.get("max_deduct")
    if max_deduct in [None, "", "无"]:
        max_deduct = float("inf")
    else:
        try:
            max_deduct = float(max_deduct)
        except Exception:
            max_deduct = float("inf")

    if ratio <= 0 or coefficient < 0:
        return

    # 1) 减少源属性
    if source == "物攻":
        src_min_key, src_max_key = "最小物攻", "最大物攻"
        src_min = calculate_dict.get(src_min_key, 0)
        src_max = calculate_dict.get(src_max_key, 0)
        deduct_min = int(min(src_min * ratio, max_deduct))
        deduct_max = int(min(src_max * ratio, max_deduct))
        calculate_dict[src_min_key] = src_min - deduct_min
        calculate_dict[src_max_key] = src_max - deduct_max
        source_for_convert = int(min(int((src_min + src_max) / 2) * ratio, max_deduct))
    elif source == "魔攻":
        src_min_key, src_max_key = "最小魔攻", "最大魔攻"
        src_min = calculate_dict.get(src_min_key, 0)
        src_max = calculate_dict.get(src_max_key, 0)
        deduct_min = int(min(src_min * ratio, max_deduct))
        deduct_max = int(min(src_max * ratio, max_deduct))
        calculate_dict[src_min_key] = src_min - deduct_min
        calculate_dict[src_max_key] = src_max - deduct_max
        source_for_convert = int(min(int((src_min + src_max) / 2) * ratio, max_deduct))
    else:
        source_key_map = {"防御": "防御", "魔防": "魔防", "致命": "致命"}
        source_key = source_key_map.get(source)
        if source_key is None:
            return
        source_now = calculate_dict.get(source_key, 0)
        source_for_convert = int(min(source_now * ratio, max_deduct))
        calculate_dict[source_key] = source_now - source_for_convert

    # 2) 增加目标属性
    gain_value = int(source_for_convert * coefficient)
    if target == "物攻":
        calculate_dict["最小物攻"] = calculate_dict.get("最小物攻", 0) + gain_value
        calculate_dict["最大物攻"] = calculate_dict.get("最大物攻", 0) + gain_value
    elif target == "魔攻":
        calculate_dict["最小魔攻"] = calculate_dict.get("最小魔攻", 0) + gain_value
        calculate_dict["最大魔攻"] = calculate_dict.get("最大魔攻", 0) + gain_value
    else:
        target_key_map = {"防御": "防御", "魔防": "魔防", "致命": "致命"}
        target_key = target_key_map.get(target)
        if target_key is None:
            return
        calculate_dict[target_key] = calculate_dict.get(target_key, 0) + gain_value


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
                    card_state,
                    player_level="50",
                    core_rune_info=None):
    """ 计算 """
    try:
        level_int = int(player_level)
    except Exception:
        level_int = 50

    res_state_dict = {"力量": 0, "敏捷": 0, "智力": 0, "体质": 0,
                      "HP": 0, "MP": 0, "MP恢复": 0, "移速": 0,
                      "最小物攻": 0, "最大物攻": 0, "最小魔攻": 0, "最大魔攻": 0,
                      "防御": 0, "魔防": 0, "致命": 0, "致命伤害": 0, "最终": 0,
                      "防御百分比": 0, "魔防百分比": 0, "致命百分比": 0, "致命伤害百分比": 0, "最终百分比": 0,
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
                      "防御": 0, "魔防": 0, "致命": 0, "致命伤害": 0, "致命伤害%": 0, "最终": 0,
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
            if state_name_now == "致命伤害" and level_int < 61:
                continue
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
                            "力量转魔攻%": 0, "智力转物攻%": 0,
                            "查克拉治愈术基础攻%": 0, "查克拉治愈术上限攻%": 0}
    calculate_skill_dict = add_dicts([calculate_skill_dict, skill_state])
    if calculate_skill_dict["查克拉治愈术基础攻%"] > 0:
        chakra_bonus = min(calculate_skill_dict["查克拉治愈术基础攻%"] +
                           int(calculate_dict["最终"] / 100) * 0.015,
                           calculate_skill_dict["查克拉治愈术上限攻%"])
        calculate_skill_dict["物攻%"] += chakra_bonus
        calculate_skill_dict["魔攻%"] += chakra_bonus
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
    _apply_core_rune_convert(calculate_dict, core_rune_info)

    for key, val in res_state_dict.items():
        if key in calculate_dict:
            if "%" not in key:
                res_state_dict[key] = int(calculate_dict[key])
            else:
                res_state_dict[key] = calculate_dict[key]

    # 修改: 使用按等级的百分比计算
    res_state_dict["防御百分比"] = calculate_defense_percent(res_state_dict["防御"], player_level=level_int)
    res_state_dict["魔防百分比"] = calculate_defense_percent(res_state_dict["魔防"], player_level=level_int)
    res_state_dict["致命百分比"] = min(calculate_critical_percent(res_state_dict["致命"], player_level=level_int) + \
                                  calculate_dict["致命面板%"] * 100, 90)
    res_state_dict["致命伤害百分比"] = calculate_critical_damage_percent(
        res_state_dict["致命伤害"], player_level=level_int
    ) + round(calculate_dict["致命伤害%"] * 100, 3)
    res_state_dict["最终百分比"] = calculate_final_atk_percent(res_state_dict["最终"], player_level=level_int)

    return res_state_dict


def dps_increase_calculate(job,
                           player_state,
                           equipment_state,
                           glyph_state,
                           glyph_names_list,
                           glyph_p_names_list,
                           expedition_part,
                           rune_list,
                           rune_board_levels,
                           rune_state,
                           skin_state,
                           surplus_state,
                           others_state,
                           skill_state,
                           association_state,
                           card_state,
                           final_state,
                           dps_list,
                           player_level="50",
                           core_rune_info=None):
    """ 计算攻击属性收益 """
    glyph_plus_dict = {"最大物攻": "三属性物攻", "最大魔攻": "三属性魔攻", "致命": "三属性致命",
                       "致命伤害": "三属性致命伤害",
                       "力量": "三属性力量", "敏捷": "三属性敏捷", "智力": "三属性智力", "最终": "三属性最终"}
    rune_dict = {"物攻": "石板物攻", "魔攻": "石板魔攻", "致命": "石板致命",
                 "力量": "石板力量", "敏捷": "石板敏捷", "智力": "石板智力",
                 "最终": "石板最终"}
    combat_dps_list, analysis_mode, replace_slot = _split_dps_analysis_inputs(dps_list)

    ori_dps = dps_func(list(combat_dps_list) + [final_state])

    res_dps_list = []

    target_slot = None
    if analysis_mode == "单槽替换" and replace_slot == "三属性纹章":
        res_glyph_list, target_slot = _get_glyph_replacement_results(
            job, player_state, equipment_state, glyph_names_list, glyph_p_names_list, expedition_part,
            rune_state, skin_state, surplus_state, others_state, skill_state, association_state, card_state,
            player_level, core_rune_info,
            lambda st: dps_func(list(combat_dps_list) + [st]),
            ori_dps, glyph_plus_dict
        )
        res_dps_list.extend(res_glyph_list)
    elif analysis_mode == "单槽替换" and replace_slot == "石板词条":
        res_rune_list, target_slot = _get_rune_replacement_results(
            job, player_state, equipment_state, glyph_state, rune_list, rune_board_levels,
            skin_state, surplus_state, others_state, skill_state, association_state, card_state,
            player_level, core_rune_info,
            lambda st: dps_func(list(combat_dps_list) + [st]),
            ori_dps, rune_dict, "atk"
        )
        res_dps_list.extend(res_rune_list)
    else:
        for key, val in glyph_plus_dict.items():
            glyph_level_key = _glyph_level_key(player_level)
            if key not in glyph_json["plus"].get(glyph_level_key, {}):
                continue
            tmp_state = add_dicts([others_state, glyph_json["plus"][glyph_level_key][key]])
            tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                              skin_state, surplus_state, tmp_state, skill_state, association_state,
                                              card_state, player_level=player_level, core_rune_info=core_rune_info)
            dps_now = dps_func(list(combat_dps_list) + [tmp_final_state])
            res_dps_list.append((round((dps_now - ori_dps) / ori_dps * 100, 2), val))
        for key, val in rune_dict.items():
            rune_val = _rune_max_value(key)
            if rune_val <= 0:
                continue
            tmp_state = add_dicts([others_state, {key: rune_val}])
            tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                              skin_state, surplus_state, tmp_state, skill_state, association_state,
                                              card_state, player_level=player_level, core_rune_info=core_rune_info)
            dps_now = dps_func(list(combat_dps_list) + [tmp_final_state])
            res_dps_list.append((round((dps_now - ori_dps) / ori_dps * 100, 2), val))

    # 输出格式规整
    # res_dps_text = f"您面对【{dps_list[-1]}】使用【{dps_list[1]}】属性【{dps_list[0]}】技能的战斗力竟然高达【{ori_dps}】! ! !"
    res_dps_text = f"您面对【{combat_dps_list[-1]}】使用\n"
    for (atk_type1_now, atk_type2_now, atk_num1_now) in [(combat_dps_list[0], combat_dps_list[1], combat_dps_list[2]),
                                                         (combat_dps_list[5], combat_dps_list[6], combat_dps_list[7]),
                                                         (combat_dps_list[10], combat_dps_list[11], combat_dps_list[12])]:
        if atk_type1_now != "无" and atk_num1_now > 0:
            res_dps_text += f"【{atk_type2_now}】属性【{atk_type1_now}】\n"
    res_dps_text += f"技能的战斗力竟然高达【{ori_dps}】! ! !"
    if analysis_mode == "单槽替换" and replace_slot == "石板词条":
        res_dps_text += "\n石板收益分析按替换【" + _describe_rune_slot(target_slot) + "】计算"
    elif analysis_mode == "单槽替换" and replace_slot == "三属性纹章":
        res_dps_text += "\n纹章收益分析按替换【" + _describe_glyph_slot(target_slot) + "】计算"

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
                           glyph_names_list,
                           glyph_p_names_list,
                           expedition_part,
                           rune_list,
                           rune_board_levels,
                           rune_state,
                           skin_state,
                           surplus_state,
                           others_state,
                           skill_state,
                           association_state,
                           card_state,
                           final_state,
                           dps_list,
                           def_type="物防",
                           player_level="50",
                           core_rune_info=None):
    """ 计算防御属性收益 """
    if def_type == "物防":
        glyph_plus_dict = {"防御": "三属性防御", "体质": "三属性体质", "HP": "三属性HP"}
        rune_dict = {"防御": "石板防御", "体质": "石板体质", "HP": "石板HP"}
    else:
        glyph_plus_dict = {"魔防": "三属性魔防", "体质": "三属性体质", "HP": "三属性HP", "智力": "三属性智力"}
        rune_dict = {"魔防": "石板魔防", "体质": "石板体质", "HP": "石板HP", "智力": "石板智力"}

    combat_dps_list, analysis_mode, replace_slot = _split_dps_analysis_inputs(dps_list)
    ori_def = def_func(list(combat_dps_list) + [final_state, def_type])

    res_def_list = []

    target_slot = None
    if analysis_mode == "单槽替换" and replace_slot == "三属性纹章":
        res_glyph_list, target_slot = _get_glyph_replacement_results(
            job, player_state, equipment_state, glyph_names_list, glyph_p_names_list, expedition_part,
            rune_state, skin_state, surplus_state, others_state, skill_state, association_state, card_state,
            player_level, core_rune_info,
            lambda st: def_func(list(combat_dps_list) + [st, def_type]),
            ori_def, glyph_plus_dict
        )
        res_def_list.extend(res_glyph_list)
    elif analysis_mode == "单槽替换" and replace_slot == "石板词条":
        rune_type = "def"
        res_rune_list, target_slot = _get_rune_replacement_results(
            job, player_state, equipment_state, glyph_state, rune_list, rune_board_levels,
            skin_state, surplus_state, others_state, skill_state, association_state, card_state,
            player_level, core_rune_info,
            lambda st: def_func(list(combat_dps_list) + [st, def_type]),
            ori_def, rune_dict, rune_type
        )
        res_def_list.extend(res_rune_list)
    else:
        for key, val in glyph_plus_dict.items():
            glyph_level_key = _glyph_level_key(player_level)
            if key not in glyph_json["plus"].get(glyph_level_key, {}):
                continue
            tmp_state = add_dicts([others_state, glyph_json["plus"][glyph_level_key][key]])
            tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                              skin_state, surplus_state, tmp_state, skill_state, association_state,
                                              card_state, player_level=player_level, core_rune_info=core_rune_info)
            def_now = def_func(list(combat_dps_list) + [tmp_final_state, def_type])
            res_def_list.append((round((def_now - ori_def) / ori_def * 100, 2), val))
        for key, val in rune_dict.items():
            rune_val = _rune_max_value(key)
            if rune_val <= 0:
                continue
            tmp_state = add_dicts([others_state, {key: rune_val}])
            tmp_final_state = state_calculate(job, player_state, equipment_state, glyph_state, rune_state,
                                              skin_state, surplus_state, tmp_state, skill_state, association_state,
                                              card_state, player_level=player_level, core_rune_info=core_rune_info)
            def_now = def_func(list(combat_dps_list) + [tmp_final_state, def_type])
            res_def_list.append((round((def_now - ori_def) / ori_def * 100, 2), val))

    # 输出格式规整
    res_def_text = f"您面对【{combat_dps_list[-1]}】的【{def_type}】生存力足足有【{ori_def}】! ! !"
    if analysis_mode == "单槽替换" and replace_slot == "石板词条":
        res_def_text += "\n石板收益分析按替换【" + _describe_rune_slot(target_slot) + "】计算"
    elif analysis_mode == "单槽替换" and replace_slot == "三属性纹章":
        res_def_text += "\n纹章收益分析按替换【" + _describe_glyph_slot(target_slot) + "】计算"
    res_def_dict_final = {"属性": [], "收益率": []}
    # res_dps_list.sort()
    for key, val in res_def_list:
        if key != 0:
            res_def_dict_final["属性"].append(val)
            res_def_dict_final["收益率"].append(key)
    df = pd.DataFrame(res_def_dict_final)
    # df_sorted = df.sort_values(by="收益率", ascending=False)

    return res_def_text, df


def get_out_format(job: str, input_dict: dict, player_level: str):
    text1 = (f"等级: {str(player_level)}\n职业: {job}\nHP: {input_dict['HP']}\nMP: {input_dict['MP']}\n"
             f"MP恢复: {input_dict['MP恢复']}")
    text2 = f"力量: {input_dict['力量']}\n敏捷: {input_dict['敏捷']}\n" \
            f"智力: {input_dict['智力']}\n体质: {input_dict['体质']}"
    text3 = f"物攻: {input_dict['最小物攻']} ~ {input_dict['最大物攻']}\n" \
            f"魔攻: {input_dict['最小魔攻']} ~ {input_dict['最大魔攻']}\n" \
            f"防御: {input_dict['防御']}  ({input_dict['防御百分比']}%)\n" \
            f"魔防: {input_dict['魔防']}  ({input_dict['魔防百分比']}%)"
    text4 = f"致命: {input_dict['致命']}  ({input_dict['致命百分比']}%)\n" \
            f"致命伤害: {input_dict['致命伤害']}  ({input_dict['致命伤害百分比']}%)\n" \
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
                     "rune_board_levels", "skin", "surplus", "other", "dps", "card_skill", "card"]
    if not all(k in segment_lengths for k in required_keys):
        return _error_return("metadata缺少必要字段")

    # 去掉 metadata 参数本体
    args = args[:-1]

    # 2. 切片
    pos = 0
    try:
        level_candidate = args[pos]; job_candidate = args[pos + 1]
        level_now = level_candidate; job_now = job_candidate; pos += 2
        equipment_list = list(args[pos: pos + segment_lengths["equipment"]]); pos += segment_lengths["equipment"]
        glyph_base_list = list(args[pos: pos + segment_lengths["glyph_base"]]); pos += segment_lengths["glyph_base"]
        glyph_plus_list = list(args[pos: pos + segment_lengths["glyph_plus"]]); pos += segment_lengths["glyph_plus"]
        rune_list = list(args[pos: pos + segment_lengths["rune"]]); pos += segment_lengths["rune"]
        rune_board_levels = list(args[pos: pos + segment_lengths["rune_board_levels"]]); pos += segment_lengths["rune_board_levels"]
        skin_list = list(args[pos: pos + segment_lengths["skin"]]); pos += segment_lengths["skin"]
        surplus_list = list(args[pos: pos + segment_lengths["surplus"]]); pos += segment_lengths["surplus"]
        others_list = list(args[pos: pos + segment_lengths["other"]]); pos += segment_lengths["other"]
        dps_list = list(args[pos: pos + segment_lengths["dps"]]); pos += segment_lengths["dps"]
        card_skill_list = list(args[pos: pos + segment_lengths["card_skill"]]); pos += segment_lengths["card_skill"]
        card_list = list(args[pos: pos + segment_lengths["card"]]); pos += segment_lengths["card"]
    except Exception as e:
        return _error_return("切片失败:" + str(e))


    # 3. 验证职业合法性
    if job_now in ["无", "请选择你的职业", "", None] or job_now not in job_info_dict2:
        return _error_return("职业未选择或非法")

    try:
        # 基础属性(带等级)
        check_level(level_now)
        player_base_state = player_base_func(job_now, level_now)
        # 装备属性
        check_equipment(equipment_list)
        equipment_state = equipment_func(job_now, equipment_list)
        # 纹章属性
        glyph_input_combined = list(glyph_base_list) + list(glyph_plus_list)
        check_glyph(glyph_input_combined)
        glyph_state = glyph_func(glyph_input_combined, player_level=level_now)
        glyph_names_list = list(glyph_base_list[:11])
        glyph_p_names_list = list(glyph_plus_list[:11])
        expedition_part = list(glyph_plus_list[11:])
        # 石板属性
        check_rune(rune_list)
        rune_state = rune_func(rune_list)  # rune_board_levels 仅用于保存/展示，不参与计算
        core_rune_info = _extract_core_rune_info(rune_list)
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
                                      others_state, skill_state, association_state, card_state,
                                      player_level=level_now, core_rune_info=core_rune_info)
        # 战斗力/防御收益
        dps_text, dps_increase_df = dps_increase_calculate(job_now,
                                                           player_base_state, equipment_state, glyph_state,
                                                           glyph_names_list, glyph_p_names_list, expedition_part,
                                                           rune_list, rune_board_levels, rune_state, skin_state, surplus_state,
                                                           others_state, skill_state, association_state,
                                                           card_state, final_state, dps_list, player_level=level_now,
                                                           core_rune_info=core_rune_info)
        def_text, def_increase_df = def_increase_calculate(job_now,
                                                           player_base_state, equipment_state, glyph_state,
                                                           glyph_names_list, glyph_p_names_list, expedition_part,
                                                           rune_list, rune_board_levels, rune_state, skin_state, surplus_state,
                                                           others_state, skill_state, association_state,
                                                           card_state, final_state, dps_list, def_type="物防",
                                                           player_level=level_now, core_rune_info=core_rune_info)
        magic_def_text, magic_def_increase_df = def_increase_calculate(job_now,
                                                                        player_base_state, equipment_state, glyph_state,
                                                                        glyph_names_list, glyph_p_names_list, expedition_part,
                                                                        rune_list, rune_board_levels, rune_state, skin_state, surplus_state,
                                                                        others_state, skill_state, association_state,
                                                                        card_state, final_state, dps_list, def_type="魔防",
                                                                        player_level=level_now,
                                                                        core_rune_info=core_rune_info)

        out_panel_text_list = get_out_format(job_now, final_state, player_level=level_now)
        check_text1 = get_check_format(glyph_state)
        check_text2 = get_check_format(card_state)
        check_text3 = get_check_format(rune_state)
        check_text4 = get_check_format(collection_state)

        logger.info("输入: " + str(args))
        return out_panel_text_list + \
               [dps_text, gr.update(value=dps_increase_df),
                def_text, gr.update(value=def_increase_df),
                magic_def_text, gr.update(value=magic_def_increase_df),
                check_text1, check_text2, check_text3, check_text4]
    except Exception as e:
        traceback.print_exc()
        return _error_return(str(e))
