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


def _create_expedition_section():
    """ 创建远征队纹章栏组件 (4种纹章, 每种的所有 base 属性独立下拉 + 共用一个 plus 下拉) """
    expedition_base_components = []  # 所有 base 数值选择组件
    expedition_plus_components = []  # 每种远征纹章的 plus 组件

    # 固定顺序使用 glyph2_json 的键顺序
    expedition_names = list(glyph2_json.keys())
    gr.Markdown("### 远征队纹章栏")
    for idx, glyph_name in enumerate(expedition_names, start=1):
        data_now = glyph2_json[glyph_name]
        base_dict = data_now.get("base", {})
        plus_dict = data_now.get("plus", {})
        with gr.Group():
            with gr.Row():
                if glyph_name == "攻击之远征队纹章":
                    merged_base = {
                        "物攻": base_dict.get("最小物攻") or base_dict.get("最大物攻") or [],
                        "魔攻": base_dict.get("最小魔攻") or base_dict.get("最大魔攻") or []
                    }
                    for attr_name, attr_values in merged_base.items():
                        comp = gr.Dropdown(["无"] + [str(v) for v in attr_values], value="无", label=f"{glyph_name}-{attr_name}")
                        expedition_base_components.append(comp)
                else:
                    for attr_name, attr_values in base_dict.items():
                        comp = gr.Dropdown(["无"] + [str(v) for v in attr_values], value="无", label=f"{glyph_name}-{attr_name}")
                        expedition_base_components.append(comp)
            # plus 属性
            plus_choices_raw = plus_dict.items()
            # 合并plus属性中的最小/最大物攻与最小/最大魔攻
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
            # 其余属性
            for k, v in plus_dict.items():
                if k in ["最小物攻", "最大物攻", "最小魔攻", "最大魔攻"]:
                    continue
                merged_plus[k] = v
            plus_choices = ["无"] + [f"{p_name}+{val}" for p_name, val in merged_plus.items()]
            plus_comp = gr.Dropdown(plus_choices, value="无", label=f"{glyph_name}-额外属性")
            expedition_plus_components.append(plus_comp)
    return expedition_base_components, expedition_plus_components


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
        expedition_base_components, expedition_plus_components = _create_expedition_section()

    hidden_components = []
    plus_components = []
    for (_lv_dd, _name_dd, plus_dd, hidden_val) in glyph_rows:
        plus_components.append(plus_dd)
        hidden_components.append(hidden_val)
    # 将远征队 base 与 plus 组件追加到 plus_components 中 (保持主流程 slice 简单)
    plus_components.extend(expedition_base_components)
    plus_components.extend(expedition_plus_components)

    return hidden_components, plus_components
