"""
战力结果
"""

import gradio as gr


def create_out_ability():
    with gr.Tab("战力"):
        gr.Markdown("### 战力计算结果")
        with gr.Row():
            dps_text = gr.TextArea("一刀秒了！", label="当前配装的战斗力", lines=4)
            dps_increase_plot = gr.BarPlot(x="属性", y="收益率", title="三属性纹章和石板攻击属性收益率",
                                           sort="-y", height=300, bar_width=0.5, x_label_angle=45)
        with gr.Row():
            def_text = gr.TextArea("神操，不会中技能！", label="当前配装的物防生存力", lines=2)
            def_increase_plot = gr.BarPlot(x="属性", y="收益率", title="三属性纹章和石板物防属性收益率",
                                           sort="-y", height=300, bar_width=0.5, x_label_angle=45)
        with gr.Row():
            magic_def_text = gr.TextArea("神操，不会中技能！", label="当前配装的魔防生存力", lines=2)
            magic_def_increase_plot = gr.BarPlot(x="属性", y="收益率", title="三属性纹章和石板魔防属性收益率",
                                                 sort="-y", height=300, bar_width=0.5, x_label_angle=45)
        with gr.Row():
            gr.Markdown("\n\n\n\n\n\n")

    return dps_text, dps_increase_plot, def_text, def_increase_plot, \
           magic_def_text, magic_def_increase_plot
