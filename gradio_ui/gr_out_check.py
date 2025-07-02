"""
属性校验
"""

import gradio as gr


def create_out_check():
    with gr.Tab("属性校验"):
        gr.Markdown("### 属性校验(框内属性过多可以滚动)")
        with gr.Row():
            check_text1 = gr.Textbox(label="纹章页汇总", autoscroll=False, lines=20)
            check_text2 = gr.Textbox(label="卡片页汇总", autoscroll=False, lines=20)
            check_text3 = gr.Textbox(label="石板页汇总", autoscroll=False, lines=20)
            check_text4 = gr.Textbox(label="时装收集汇总", autoscroll=False, lines=20)
        with gr.Row():
            gr.Markdown("\n\n\n\n\n\n")

    return check_text1, check_text2, check_text3, check_text4
