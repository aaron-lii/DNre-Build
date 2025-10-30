"""
纹章页
"""

import gradio as gr

from src.tool_func import rune_json


def get_rune_data(default_level: str = None):
    """ 获取石板（攻击/防御）名称列表, 基于指定等级(默认取最小等级) """
    level_keys = sorted(rune_json.keys(), key=lambda x: int(x)) if isinstance(rune_json, dict) else []
    if not level_keys:
        return ["无"], ["无"], []
    if default_level is None or default_level not in level_keys:
        default_level = level_keys[0]
    atk_names = ["无"] + list(rune_json[default_level]["atk"].keys())
    def_names = ["无"] + list(rune_json[default_level]["def"].keys())
    return atk_names, def_names, level_keys


def _build_value_choices(level: str, rune_name: str, rune_type: str):
    """ 根据等级/名称/类型返回属性数值choices(str list)。"""
    if rune_name in ["无", "", None]:
        return ["无"]
    try:
        vals = rune_json[level][rune_type][rune_name]
        return [str(v) for v in vals]
    except Exception:
        return ["无"]


def update_atk_rune(level, rune_name):
    """更新攻击石板 名称下拉(以防等级切换导致可选项变更) 与 数值下拉。"""
    level = str(level)
    # 名称可选项
    atk_names = ["无"]
    try:
        atk_names += list(rune_json[level]["atk"].keys())
    except Exception:
        pass
    # 若当前名称不在可选项, 重置为"无"
    if rune_name not in atk_names:
        rune_name = atk_names[0]
    value_choices = _build_value_choices(level, rune_name, "atk")
    return gr.update(choices=atk_names, value=rune_name), gr.update(choices=value_choices, value=value_choices[-1])


def update_def_rune(level, rune_name):
    """更新防御石板 名称与数值。"""
    level = str(level)
    def_names = ["无"]
    try:
        def_names += list(rune_json[level]["def"].keys())
    except Exception:
        pass
    if rune_name not in def_names:
        rune_name = def_names[0]
    value_choices = _build_value_choices(level, rune_name, "def")
    return gr.update(choices=def_names, value=rune_name), gr.update(choices=value_choices, value=value_choices[-1])


# 新增: 板级别批量更新函数（等级改变时一次性更新该板 6 条属性的 名称choices 与 数值choices）
def update_board_atk(level, *names):
    level = str(level)
    outputs = []
    for name in names:
        name_upd, val_upd = update_atk_rune(level, name)
        outputs.append(name_upd)
        outputs.append(val_upd)
    return outputs


def update_board_def(level, *names):
    level = str(level)
    outputs = []
    for name in names:
        name_upd, val_upd = update_def_rune(level, name)
        outputs.append(name_upd)
        outputs.append(val_upd)
    return outputs


def create_rune_tab():
    """ 为每块石板新增 单一等级下拉 (4 个板), 不改变返回格式: 24 名称 + 24 数值。额外返回4个板等级组件供保存/加载使用 """
    tmp_list = ["无"]
    atk_rune_name_list, def_rune_name_list, level_keys = get_rune_data()
    default_level = level_keys[0] if level_keys else "50"

    with gr.Tab("石板页"):
        with gr.Row():
            # 攻击石板1
            with gr.Column():
                gr.Markdown("### 攻击石板1")
                atk_board1_level = gr.Dropdown(level_keys, value=default_level, label="石板等级")
                with gr.Row():
                    rune1 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条1")
                    rune1_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条1属性")
                with gr.Row():
                    rune2 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条2")
                    rune2_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条2属性")
                with gr.Row():
                    rune3 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条3")
                    rune3_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条3属性")
                with gr.Row():
                    rune4 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条4")
                    rune4_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条4属性")
                with gr.Row():
                    rune17 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条5")
                    rune17_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条5属性")
                with gr.Row():
                    rune18 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条6")
                    rune18_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条6属性")
            # 攻击石板2
            with gr.Column():
                gr.Markdown("### 攻击石板2")
                atk_board2_level = gr.Dropdown(level_keys, value=default_level, label="石板等级")
                with gr.Row():
                    rune5 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条1")
                    rune5_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条1属性")
                with gr.Row():
                    rune6 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条2")
                    rune6_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条2属性")
                with gr.Row():
                    rune7 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条3")
                    rune7_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条3属性")
                with gr.Row():
                    rune8 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条4")
                    rune8_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条4属性")
                with gr.Row():
                    rune19 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条5")
                    rune19_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条5属性")
                with gr.Row():
                    rune20 = gr.Dropdown(atk_rune_name_list, value=atk_rune_name_list[0], label="词条6")
                    rune20_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条6属性")
        gr.Markdown("---")
        with gr.Row():
            # 防御石板1
            with gr.Column():
                gr.Markdown("### 防御石板1")
                def_board1_level = gr.Dropdown(level_keys, value=default_level, label="石板等级")
                with gr.Row():
                    rune9 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条1")
                    rune9_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条1属性")
                with gr.Row():
                    rune10 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条2")
                    rune10_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条2属性")
                with gr.Row():
                    rune11 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条3")
                    rune11_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条3属性")
                with gr.Row():
                    rune12 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条4")
                    rune12_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条4属性")
                with gr.Row():
                    rune21 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条5")
                    rune21_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条5属性")
                with gr.Row():
                    rune22 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条6")
                    rune22_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条6属性")
            # 防御石板2
            with gr.Column():
                gr.Markdown("### 防御石板2")
                def_board2_level = gr.Dropdown(level_keys, value=default_level, label="石板等级")
                with gr.Row():
                    rune13 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条1")
                    rune13_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条1属性")
                with gr.Row():
                    rune14 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条2")
                    rune14_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条2属性")
                with gr.Row():
                    rune15 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条3")
                    rune15_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条3属性")
                with gr.Row():
                    rune16 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条4")
                    rune16_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条4属性")
                with gr.Row():
                    rune23 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条5")
                    rune23_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条5属性")
                with gr.Row():
                    rune24 = gr.Dropdown(def_rune_name_list, value=def_rune_name_list[0], label="词条6")
                    rune24_p = gr.Dropdown(tmp_list, value=tmp_list[0], label="词条6属性")

    # 属性分组
    atk_board1_names = [rune1, rune2, rune3, rune4, rune17, rune18]
    atk_board1_vals = [rune1_p, rune2_p, rune3_p, rune4_p, rune17_p, rune18_p]
    atk_board2_names = [rune5, rune6, rune7, rune8, rune19, rune20]
    atk_board2_vals = [rune5_p, rune6_p, rune7_p, rune8_p, rune19_p, rune20_p]
    def_board1_names = [rune9, rune10, rune11, rune12, rune21, rune22]
    def_board1_vals = [rune9_p, rune10_p, rune11_p, rune12_p, rune21_p, rune22_p]
    def_board2_names = [rune13, rune14, rune15, rune16, rune23, rune24]
    def_board2_vals = [rune13_p, rune14_p, rune15_p, rune16_p, rune23_p, rune24_p]

    # 事件: 板等级变化 -> 批量更新
    atk_board1_level.change(update_board_atk, inputs=[atk_board1_level] + atk_board1_names, outputs=[v for pair in zip(atk_board1_names, atk_board1_vals) for v in pair])
    atk_board2_level.change(update_board_atk, inputs=[atk_board2_level] + atk_board2_names, outputs=[v for pair in zip(atk_board2_names, atk_board2_vals) for v in pair])
    def_board1_level.change(update_board_def, inputs=[def_board1_level] + def_board1_names, outputs=[v for pair in zip(def_board1_names, def_board1_vals) for v in pair])
    def_board2_level.change(update_board_def, inputs=[def_board2_level] + def_board2_names, outputs=[v for pair in zip(def_board2_names, def_board2_vals) for v in pair])

    # 事件: 名称变化 -> 单条更新 (依赖所属板等级)
    for name_comp, val_comp in zip(atk_board1_names, atk_board1_vals):
        name_comp.change(update_atk_rune, inputs=[atk_board1_level, name_comp], outputs=[name_comp, val_comp])
    for name_comp, val_comp in zip(atk_board2_names, atk_board2_vals):
        name_comp.change(update_atk_rune, inputs=[atk_board2_level, name_comp], outputs=[name_comp, val_comp])
    for name_comp, val_comp in zip(def_board1_names, def_board1_vals):
        name_comp.change(update_def_rune, inputs=[def_board1_level, name_comp], outputs=[name_comp, val_comp])
    for name_comp, val_comp in zip(def_board2_names, def_board2_vals):
        name_comp.change(update_def_rune, inputs=[def_board2_level, name_comp], outputs=[name_comp, val_comp])

    # 返回顺序保持不变 (仅名称 + 数值)
    rune_return_list = atk_board1_names + atk_board2_names + def_board1_names + def_board2_names + \
           atk_board1_vals + atk_board2_vals + def_board1_vals + def_board2_vals
    board_levels = [atk_board1_level, atk_board2_level, def_board1_level, def_board2_level]
    return rune_return_list, board_levels
