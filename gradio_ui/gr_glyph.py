"""
纹章页
"""

import gradio as gr

from src.tool_func import glyph_json

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


def create_glyph_tab():
    """ gr页面：返回原保存格式组件列表 (hidden) + 三属性列表，接口兼容 """
    with gr.Tab("纹章页"):
        gr.Markdown("### 基础纹章栏")
        glyph_rows = []
        for i in range(1, 9):
            glyph_rows.append(create_glyph_row(i))
        gr.Markdown("---")
        gr.Markdown("### 额外纹章栏")
        for i in range(9, 12):
            glyph_rows.append(create_glyph_row(i))

    hidden_components = []
    plus_components = []
    for (_lv_dd, _name_dd, plus_dd, hidden_val) in glyph_rows:
        plus_components.append(plus_dd)
        hidden_components.append(hidden_val)

    return hidden_components, plus_components
