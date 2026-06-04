"""
skin页
"""

import json
import re
import gradio as gr
from collections import defaultdict
from typing import Optional

from src.tool_func import skin_json, equipment_base_json, job_info_dict2, job_info_dict

UNIVERSAL_WEAPON1_SKINS = {"黑暗灵魂(属性提升)", "光明、紫魅、圣诞、黑暗"}
UNIVERSAL_WEAPON2_SKINS = {"黑暗灵魂(属性提升)", "光明、紫魅、圣诞、黑暗"}
PROTECTED_SKIN_FAMILIES = {
    "圣诞噩梦",
    "夜空降临",
    "祝福婚礼",
    "地狱幽冥鬼火",
    "涅火凤羽流萤",
}

WEAPON_TOKENS = [
    "长剑", "短剑", "锤子", "斧头", "偃月刀",
    "长弓", "短弓", "十字弓",
    "书", "人偶", "宝珠",
    "法杖", "权杖", "魔杖",
    "连枷", "卡巴拉", "加农炮", "查克拉姆", "扇子",
]

WEAPON_TOKENS_EXTRA = [
    "护手", "箭筒", "盾牌",
    "穿线环", "护身符", "符咒", "曲柄杖",
]
SKIN_PART_TOKENS = WEAPON_TOKENS + WEAPON_TOKENS_EXTRA + [
    "魔法书", "翅膀", "尾巴", "尾饰", "印花", "纹身",
    "项链", "耳环", "戒指",
]
SKIN_KEYS = [
    "weapon1_skin", "weapon2_skin", "wing_skin", "tail_skin",
    "printing_skin", "necklace_skin", "earrings_skin", "ring_skin",
]


def _resolve_base_job(job: str):
    """将高阶职业映射到基础职业。"""
    if job in ["无", "", None, "请选择你的职业"]:
        return None
    mid_job = job_info_dict2.get(job)
    if not mid_job:
        return None
    return job_info_dict.get(mid_job)


def _collect_weapon_tokens(job: str):
    """根据当前职业收集允许的武器类型关键字。"""
    base_job = _resolve_base_job(job)
    if not base_job:
        return set()
    tokens = set()
    for job_key in [base_job, job_info_dict2.get(job)]:
        if not job_key:
            continue
        for lv_map in equipment_base_json.get(job_key, {}).values():
            for equip_name, meta in lv_map.items():
                part_now = str(meta.get("部位", "")).split("-", 1)[0]
                if part_now not in {"主手", "副手"}:
                    continue
                for token in WEAPON_TOKENS + WEAPON_TOKENS_EXTRA:
                    if token in equip_name:
                        tokens.add(token)
    return tokens


def _filter_skin_names(job: str, skin_key: str, token_pool: set[str], universal_names: set[str]):
    """按职业过滤武器类时装。"""
    names = []
    data = skin_json.get(skin_key, {})
    if not job or job in ["无", "请选择你的职业", ""]:
        names.extend(list(data.keys()))
        return names
    for name in data.keys():
        if re.fullmatch(r"\{.*\}", name):
            continue
        if any(token in name for token in token_pool):
            names.append(name)
            continue
        if name in universal_names:
            names.append(name)
    return names


def _extract_skin_family(name: str):
    family = re.sub(r"\([^)]*\)", "", name)
    family = family.replace("[进化]", "").replace("同类", "")
    for token in SKIN_PART_TOKENS:
        family = family.replace(token, "")
    family = family.replace("之", "").replace("的", "")
    return re.sub(r"\s+", "", family)


def _is_merge_protected(name: str):
    return _extract_skin_family(name) in PROTECTED_SKIN_FAMILIES


def _build_merged_label(name: str, count: int):
    return f"{name} 等{count}款（同属性）"


def _build_skin_choices(skin_key: str, names: list[str]):
    state_groups = defaultdict(list)
    for name in names:
        state_groups[json.dumps(skin_json[skin_key][name], ensure_ascii=False, sort_keys=True)].append(name)

    alias_map = {}
    merged_group_map = {}
    for group_names in state_groups.values():
        mergeable_names = [name for name in group_names if not _is_merge_protected(name)]
        if len(mergeable_names) <= 1:
            continue
        representative = mergeable_names[0]
        merged_group_map[representative] = mergeable_names
        for name in mergeable_names:
            alias_map[name] = representative

    choices = ["无"]
    emitted_names = set()
    for name in names:
        if name in emitted_names:
            continue
        if name in merged_group_map:
            choices.append((_build_merged_label(name, len(merged_group_map[name])), name))
            emitted_names.update(merged_group_map[name])
            continue
        if name in alias_map:
            continue
        choices.append(name)
        emitted_names.add(name)

    return choices, alias_map


def get_skin_option_data(job: Optional[str] = None):
    weapon_tokens = _collect_weapon_tokens(job)
    visible_name_map = {
        "weapon1_skin": _filter_skin_names(job, "weapon1_skin", weapon_tokens, UNIVERSAL_WEAPON1_SKINS),
        "weapon2_skin": _filter_skin_names(job, "weapon2_skin", weapon_tokens, UNIVERSAL_WEAPON2_SKINS),
        "wing_skin": list(skin_json["wing_skin"].keys()),
        "tail_skin": list(skin_json["tail_skin"].keys()),
        "printing_skin": list(skin_json["printing_skin"].keys()),
        "necklace_skin": list(skin_json["necklace_skin"].keys()),
        "earrings_skin": list(skin_json["earrings_skin"].keys()),
        "ring_skin": list(skin_json["ring_skin"].keys()),
    }

    option_data = {}
    for skin_key in SKIN_KEYS:
        choices, alias_map = _build_skin_choices(skin_key, visible_name_map[skin_key])
        option_data[skin_key] = {
            "choices": choices,
            "alias_map": alias_map,
        }
    return option_data


def normalize_skin_selection(job: Optional[str], skin_key: str, value: str):
    if value in ["", None]:
        return "无"

    option_data = get_skin_option_data(job).get(skin_key, {})
    if value == "无":
        return "无"
    if value in option_data.get("alias_map", {}):
        return option_data["alias_map"][value]

    for choice in option_data.get("choices", []):
        if isinstance(choice, tuple):
            if choice[1] == value:
                return value
        elif choice == value:
            return value
    return "无"


def get_skin_data(job: Optional[str] = None):
    """ 获取时装数据 """
    option_data = get_skin_option_data(job)
    return [option_data[skin_key]["choices"] for skin_key in SKIN_KEYS]


def update_skin_options(job: str):
    """ 根据职业刷新武器/副手时装选项 """
    weapon1_skin_list, weapon2_skin_list, *_ = get_skin_data(job)
    return [
        gr.update(choices=weapon1_skin_list, value="无"),
        gr.update(choices=weapon2_skin_list, value="无"),
    ]


def create_skin_tab():
    [weapon1_skin_list, weapon2_skin_list, wing_skin_list,
     tail_skin_list, printing_skin_list, necklace_skin_list,
     earrings_skin_list, ring_skin_list] = get_skin_data()

    with gr.Tab("时装页"):
        gr.Markdown("### 五件套")
        with gr.Row():
            with gr.Column():
                weapon1_skin = gr.Dropdown(weapon1_skin_list, label="主手")
                weapon2_skin = gr.Dropdown(weapon2_skin_list, label="副手")
            with gr.Column():
                wing_skin = gr.Dropdown(wing_skin_list, label="翅膀")
                printing_skin = gr.Dropdown(printing_skin_list, label="印花")
                tail_skin = gr.Dropdown(tail_skin_list, label="尾巴")
        gr.Markdown("---")
        gr.Markdown("### 首饰")
        with gr.Row():
            with gr.Column():
                necklace_skin = gr.Dropdown(necklace_skin_list, label="项链")
                earrings_skin = gr.Dropdown(earrings_skin_list, label="耳环")
            with gr.Column():
                ring1_skin = gr.Dropdown(ring_skin_list, label="戒指1")
                ring2_skin = gr.Dropdown(ring_skin_list, label="戒指2")

    return [weapon1_skin, weapon2_skin,
            wing_skin, tail_skin, printing_skin,
            necklace_skin, earrings_skin, ring1_skin, ring2_skin]
