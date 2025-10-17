"""
纹章页
"""

import gradio as gr

from src.tool_func import rune_json


def get_rune_data():
    """ 获取石板数据 """
    atk_rune_name_list = ["无"]
    def_rune_name_list = ["无"]

    atk_rune_name_list += list(rune_json["atk"].keys())
    def_rune_name_list += list(rune_json["def"].keys())

    return atk_rune_name_list, def_rune_name_list


def update_rune_options(rune_input):
    """ 根据rune更新随机属性选项 """
    state_list = ["无"]
    for rune_type, val1 in rune_json.items():
        if rune_input in val1:
            state_list = rune_json[rune_type][rune_input]
            for i in range(len(state_list)):
                state_list[i] = str(state_list[i])

    return gr.update(choices=state_list, value=state_list[-1])


def create_rune_tab():
    """ gr页面 """
    tmp_list = ["无"]
    atk_rune_name_list, def_rune_name_list = get_rune_data()

    with gr.Tab("石板页"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 攻击石板1")
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
            with gr.Column():
                gr.Markdown("### 攻击石板2")
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
            with gr.Column():
                gr.Markdown("### 防御石板1")
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
            with gr.Column():
                gr.Markdown("### 防御石板2")
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

    atk_rune_list = [rune1, rune2, rune3, rune4, rune17, rune18,
                     rune5, rune6, rune7, rune8, rune19, rune20]
    atk_rune_p_list = [rune1_p, rune2_p, rune3_p, rune4_p, rune17_p, rune18_p,
                       rune5_p, rune6_p, rune7_p, rune8_p, rune19_p, rune20_p]
    def_rune_list = [rune9, rune10, rune11, rune12, rune21, rune22,
                     rune13, rune14, rune15, rune16, rune23, rune24]
    def_rune_p_list = [rune9_p, rune10_p, rune11_p, rune12_p, rune21_p, rune22_p,
                       rune13_p, rune14_p, rune15_p, rune16_p, rune23_p, rune24_p]

    # 实时更新随机属性
    rune1.change(update_rune_options, inputs=[rune1], outputs=[rune1_p])
    rune2.change(update_rune_options, inputs=[rune2], outputs=[rune2_p])
    rune3.change(update_rune_options, inputs=[rune3], outputs=[rune3_p])
    rune4.change(update_rune_options, inputs=[rune4], outputs=[rune4_p])
    rune5.change(update_rune_options, inputs=[rune5], outputs=[rune5_p])
    rune6.change(update_rune_options, inputs=[rune6], outputs=[rune6_p])
    rune7.change(update_rune_options, inputs=[rune7], outputs=[rune7_p])
    rune8.change(update_rune_options, inputs=[rune8], outputs=[rune8_p])
    rune9.change(update_rune_options, inputs=[rune9], outputs=[rune9_p])
    rune10.change(update_rune_options, inputs=[rune10], outputs=[rune10_p])
    rune11.change(update_rune_options, inputs=[rune11], outputs=[rune11_p])
    rune12.change(update_rune_options, inputs=[rune12], outputs=[rune12_p])
    rune13.change(update_rune_options, inputs=[rune13], outputs=[rune13_p])
    rune14.change(update_rune_options, inputs=[rune14], outputs=[rune14_p])
    rune15.change(update_rune_options, inputs=[rune15], outputs=[rune15_p])
    rune16.change(update_rune_options, inputs=[rune16], outputs=[rune16_p])
    rune17.change(update_rune_options, inputs=[rune17], outputs=[rune17_p])
    rune18.change(update_rune_options, inputs=[rune18], outputs=[rune18_p])
    rune19.change(update_rune_options, inputs=[rune19], outputs=[rune19_p])
    rune20.change(update_rune_options, inputs=[rune20], outputs=[rune20_p])
    rune21.change(update_rune_options, inputs=[rune21], outputs=[rune21_p])
    rune22.change(update_rune_options, inputs=[rune22], outputs=[rune22_p])
    rune23.change(update_rune_options, inputs=[rune23], outputs=[rune23_p])
    rune24.change(update_rune_options, inputs=[rune24], outputs=[rune24_p])

    return atk_rune_list + def_rune_list + atk_rune_p_list + def_rune_p_list
