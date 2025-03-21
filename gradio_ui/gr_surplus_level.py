"""
surplus_level
"""

import gradio as gr


def create_surplus_level_tab():
    with gr.Tab("综合等级"):
        with gr.Row():
            property1_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="伤害增加")
            property2_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="受伤减少")
        with gr.Row():
            property3_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="最大生命值")
            property4_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="最大魔法值")
        with gr.Row():
            property5_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="物理攻击力")
            property6_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="魔法攻击力")
        with gr.Row():
            property7_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="物理防御")
            property8_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="魔法防御")
        with gr.Row():
            property9_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="致命一击")
            property10_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="最终伤害")
        with gr.Row():
            property11_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="致命一击抵抗")
            property12_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="魔法值恢复")
        with gr.Row():
            property13_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="硬直")
            property14_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="硬直抵抗")
        with gr.Row():
            property15_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="眩晕")
            property16_levle = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="眩晕抵抗")

    return [property1_levle, property2_levle, property3_levle, property4_levle,
            property5_levle, property6_levle, property7_levle, property8_levle,
            property9_levle, property10_levle, property11_levle, property12_levle,
            property13_levle, property14_levle, property15_levle, property16_levle]