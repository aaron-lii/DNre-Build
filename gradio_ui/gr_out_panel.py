"""
面板结果
"""

import gradio as gr


def create_out_panel():
    with gr.Tab("面板"):
        gr.Markdown("### 面板计算结果")
        with gr.Row():
            out_text1 = gr.Textbox(label="基础信息", lines=4)
            out_text2 = gr.Textbox(label="属性信息", lines=4)
        with gr.Row():
            out_text3 = gr.Textbox(label="一般信息", lines=4)
            out_text4 = gr.Textbox(label="特殊攻击信息", lines=4)
        with gr.Row():
            out_text5 = gr.Textbox(label="属性攻击信息", lines=4)
            out_text6 = gr.Textbox(label="属性防御信息", lines=4)
        with gr.Row():
            out_text7 = gr.Textbox(label="特殊防御信息", lines=4)
            out_text8 = gr.Textbox(label="其他信息", lines=4)
        with gr.Row():
            gr.Markdown("\n\n\n\n\n\n")

    return out_text1, out_text2, out_text3, out_text4, \
           out_text5, out_text6, out_text7, out_text8
