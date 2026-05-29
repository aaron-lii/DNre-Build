"""
纹章页
"""

import gradio as gr

from src.tool_func import glyph_json, glyph2_json

# 等级列表（保持原有顺序）
GLYPH_LEVELS = list(glyph_json["base"].keys())  # 如 ["40A", "50A"]

# 计算最高等级（按数字部分比较）
def _level_numeric(lv: str) -> int:
    num = ''.join(ch for ch in lv if ch.isdigit())
    return int(num) if num else 0
HIGHEST_LEVEL = max(GLYPH_LEVELS, key=_level_numeric) if GLYPH_LEVELS else ""

# 使用最高等级的名称与三属性列表（用户确认各等级一致）
GLYPH_BASE_NAMES = sorted(glyph_json["base"][HIGHEST_LEVEL].keys()) if HIGHEST_LEVEL else []
GLYPH_PLUS_NAMES = sorted(glyph_json["plus"][HIGHEST_LEVEL].keys()) if HIGHEST_LEVEL else []


def _expedition_level_numeric(level_key: str) -> int:
    digits = ''.join(ch for ch in str(level_key) if ch.isdigit())
    return int(digits) if digits else 0


def _is_multi_level_expedition_data():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return False
    first_key = next(iter(glyph2_json.keys()))
    first_val = glyph2_json[first_key]
    return isinstance(first_val, dict) and "base" not in first_val and "plus" not in first_val


def get_expedition_level_keys():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return []
    if _is_multi_level_expedition_data():
        return sorted(glyph2_json.keys(), key=_expedition_level_numeric)
    return ["默认"]


def get_default_expedition_level_key():
    level_keys = get_expedition_level_keys()
    return level_keys[-1] if level_keys else "默认"


def get_expedition_names():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return []
    if _is_multi_level_expedition_data():
        level_keys = get_expedition_level_keys()
        if not level_keys:
            return []
        return list(glyph2_json[level_keys[0]].keys())
    return list(glyph2_json.keys())


def get_expedition_level_data(level_key: str):
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return {}
    if _is_multi_level_expedition_data():
        level_keys = get_expedition_level_keys()
        if level_key not in level_keys:
            level_key = get_default_expedition_level_key()
        return glyph2_json.get(level_key, {})
    return glyph2_json


def _merge_expedition_plus(plus_dict: dict):
    merged_plus = {}
    min_phys = plus_dict.get("最小物攻")
    max_phys = plus_dict.get("最大物攻")
    if min_phys is not None and max_phys is not None and min_phys == max_phys:
        merged_plus["物攻"] = min_phys
    else:
        if min_phys is not None:
            merged_plus["最小物攻"] = min_phys
        if max_phys is not None:
            merged_plus["最大物攻"] = max_phys
    min_mag = plus_dict.get("最小魔攻")
    max_mag = plus_dict.get("最大魔攻")
    if min_mag is not None and max_mag is not None and min_mag == max_mag:
        merged_plus["魔攻"] = min_mag
    else:
        if min_mag is not None:
            merged_plus["最小魔攻"] = min_mag
        if max_mag is not None:
            merged_plus["最大魔攻"] = max_mag
    for k, v in plus_dict.items():
        if k in ["最小物攻", "最大物攻", "最小魔攻", "最大魔攻"]:
            continue
        merged_plus[k] = v
    return merged_plus


def get_expedition_field_defs(glyph_name: str, level_key: str):
    expedition_data = get_expedition_level_data(level_key)
    data_now = expedition_data.get(glyph_name, {})
    base_dict = data_now.get("base", {})
    plus_dict = data_now.get("plus", {})

    field_defs = [{"kind": "level", "label": "等级", "choices": get_expedition_level_keys() or ["默认"]}]
    if glyph_name == "攻击之远征队纹章":
        merged_base = {
            "物攻": base_dict.get("最小物攻") or base_dict.get("最大物攻") or [],
            "魔攻": base_dict.get("最小魔攻") or base_dict.get("最大魔攻") or [],
        }
        for attr_name, attr_values in merged_base.items():
            field_defs.append({"kind": "base", "label": attr_name, "choices": ["无"] + [str(v) for v in attr_values]})
    else:
        for attr_name, attr_values in base_dict.items():
            field_defs.append({"kind": "base", "label": attr_name, "choices": ["无"] + [str(v) for v in attr_values]})

    merged_plus = _merge_expedition_plus(plus_dict)
    field_defs.append({
        "kind": "plus",
        "label": "额外属性",
        "choices": ["无"] + [f"{p_name}+{val}" for p_name, val in merged_plus.items()],
    })
    return field_defs


def get_expedition_choice_lists(level_values=None):
    expedition_names = get_expedition_names()
    default_level_key = get_default_expedition_level_key()
    choices = []
    if level_values is None:
        level_values = [default_level_key] * len(expedition_names)
    for idx, glyph_name in enumerate(expedition_names):
        level_key = level_values[idx] if idx < len(level_values) else default_level_key
        for field_def in get_expedition_field_defs(glyph_name, level_key):
            choices.append(field_def["choices"])
    return choices


def get_glyph_data():
    """ 获取纹章数据（保持原有返回格式：所有 等级-名称 组合列表 + 三属性名称列表） """
    glyph_base_list = ["无"]
    for lev, em_dic in glyph_json["base"].items():
        for em_name in em_dic.keys():
            glyph_base_list.append(f"{lev}-{em_name}")
    glyph_base_list = ["无"] + sorted(glyph_base_list[1:])
    glyph_plus_list = ["无"] + GLYPH_PLUS_NAMES  # 三属性使用最高等级列表
    return glyph_base_list, glyph_plus_list


def combine_glyph(level, name):
    """ 组合等级与名称形成原始保存格式的字符串 """
    if level in ["无", "", None] or name in ["无", "", None]:
        return "无"
    return f"{level}-{name}"


def split_glyph(combined):
    """ 从组合值解析回 level 和 name（不更新 choices，使用固定列表） """
    if combined in ["无", "", None]:
        return gr.update(value=HIGHEST_LEVEL), gr.update(value="无")
    try:
        lv, name = combined.split("-", 1)
        # 不做存在性校验（用户保证一致），若等级不存在回退最高等级
        if lv not in GLYPH_LEVELS:
            lv = HIGHEST_LEVEL
        if name not in GLYPH_BASE_NAMES:
            name = "无"
        return gr.update(value=lv), gr.update(value=name)
    except Exception:
        return gr.update(value=HIGHEST_LEVEL), gr.update(value="无")


def create_glyph_row(idx):
    """ 创建单行纹章组件 (等级 + 名称 + 三属性 + 隐藏组合值) """
    with gr.Row():
        default_level = HIGHEST_LEVEL
        level_dd = gr.Dropdown(GLYPH_LEVELS, value=default_level, label=f"纹章{idx}等级", allow_custom_value=False)
        name_dd = gr.Dropdown(["无"] + GLYPH_BASE_NAMES, value="无", label=f"纹章{idx}")
        plus_dd = gr.Dropdown(["无"] + GLYPH_PLUS_NAMES, value="无", label=f"纹章{idx}三属性")
        hidden_val = gr.Textbox(value="无", label=f"glyph{idx}_hidden", visible=False)

        # 等级或名称变化 -> 更新隐藏组合值
        level_dd.change(combine_glyph, inputs=[level_dd, name_dd], outputs=[hidden_val])
        name_dd.change(combine_glyph, inputs=[level_dd, name_dd], outputs=[hidden_val])
        hidden_val.change(split_glyph, inputs=[hidden_val], outputs=[level_dd, name_dd])

    return level_dd, name_dd, plus_dd, hidden_val


def update_single_expedition_options(level_key: str, glyph_name: str, *current_values):
    """根据单个远征队纹章等级刷新其选项。"""
    updates = []
    field_defs = get_expedition_field_defs(glyph_name, level_key)
    normalized_level = level_key if level_key in field_defs[0]["choices"] else get_default_expedition_level_key()
    for idx, field_def in enumerate(field_defs):
        if idx == 0:
            updates.append(gr.update(choices=field_def["choices"], value=normalized_level))
            continue
        value_now = current_values[idx - 1] if idx - 1 < len(current_values) else "无"
        if value_now not in field_def["choices"]:
            value_now = "无"
        updates.append(gr.update(choices=field_def["choices"], value=value_now))
    return updates


def _create_expedition_section():
    """ 创建远征队纹章栏组件 (4种纹章, 每种的所有 base 属性独立下拉 + 共用一个 plus 下拉) """
    expedition_components = []
    expedition_names = get_expedition_names()
    default_level_key = get_default_expedition_level_key()
    gr.Markdown("### 远征队纹章栏")
    for idx, glyph_name in enumerate(expedition_names, start=1):
        field_defs = get_expedition_field_defs(glyph_name, default_level_key)
        with gr.Group():
            with gr.Row():
                section_components = []
                for field_def in field_defs:
                    default_value = default_level_key if field_def["kind"] == "level" else "无"
                    comp = gr.Dropdown(
                        field_def["choices"],
                        value=default_value,
                        label=f"{glyph_name}-{field_def['label']}",
                    )
                    section_components.append(comp)
                    expedition_components.append(comp)
            section_components[0].change(
                lambda level_key, *vals, glyph_name_now=glyph_name: update_single_expedition_options(level_key, glyph_name_now, *vals),
                inputs=[section_components[0]] + section_components[1:],
                outputs=section_components,
            )
    return expedition_components


def create_glyph_tab():
    """ gr页面：返回原保存格式组件列表 (hidden) + 三属性列表 + 远征队组件，接口兼容
    返回: hidden_components, plus_components (后者包含原三属性 + 远征队 base + 远征队 plus)
    """
    with gr.Tab("纹章页"):
        gr.Markdown("### 基础纹章栏")
        glyph_rows = []
        for i in range(1, 9):
            glyph_rows.append(create_glyph_row(i))
        gr.Markdown("---")
        gr.Markdown("### 额外纹章栏")
        for i in range(9, 12):
            glyph_rows.append(create_glyph_row(i))
        gr.Markdown("---")
        # 新增远征队纹章栏
        expedition_components = _create_expedition_section()

    hidden_components = []
    plus_components = []
    for (_lv_dd, _name_dd, plus_dd, hidden_val) in glyph_rows:
        plus_components.append(plus_dd)
        hidden_components.append(hidden_val)
    plus_components.extend(expedition_components)

    return hidden_components, plus_components, expedition_components
