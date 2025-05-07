"""
页面
"""
print("DNre配装器启动中...")
import os
import gradio as gr
import warnings
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms

from gradio_ui.gr_main import create_main_tab
from gradio_ui.gr_equipment import create_equipment_tab, update_equipment_options
from gradio_ui.gr_glyph import create_glyph_tab
from gradio_ui.gr_rune import create_rune_tab
from gradio_ui.gr_skin import create_skin_tab
from gradio_ui.gr_surplus_level import create_surplus_level_tab
from gradio_ui.gr_others import create_others_tab, update_skill_options
from gradio_ui.save_load import save_options, load_options, load_options2
from gradio_ui.gr_dps import create_dps_tab, update_dps_options
from gradio_ui.gr_card import create_card_tab
from src.main_calculate import main_func
from src.tool_func import get_my_path, version, env_now

# 捕获并忽略 "not in the list of choices" 警告
warnings.filterwarnings("ignore", message=".*not in the list of choices.*", category=UserWarning)


def update_all(job_input):
    """ 更新由于job不同改变的选项 """
    # 对于装备的变更
    change1 = update_equipment_options(job_input)
    # 对于技能的变更
    change2 = update_skill_options(job_input)
    # 对于输出类型的变更
    change3 = update_dps_options(job_input)

    return change1 + change2 + change3


def logo():
    with antd.Typography.Title(level=1,
                               elem_style=dict(fontSize=24,
                                               padding=8,
                                               margin=0,
                                               fontWeight='bold')):
        with antd.Flex(align="center", gap="small", justify="left"):
            antd.Image(os.path.join(os.path.dirname(__file__), "data/logo2.ico"),
                       preview=False,
                       alt="logo",
                       width=42,
                       height=42)
            ms.Span(f"DN怀旧服 50级配装模拟器{version}")


# 自定义 CSS，隐藏默认页脚并添加新的透明背景页脚样式
custom_css = """
footer {display: none !important;}
.custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background-color: rgba(241, 241, 241, 0.3);  /* 半透明背景 */
    font-size: 14px;
    color: #555;
}
.custom-footer a {
    color: #007bff;
    text-decoration: none;
}
.custom-footer a:hover {
    text-decoration: underline;
}
"""

# 自定义 HTML，添加新的页脚内容
custom_html = """
<div class="custom-footer">
    <p>由DN聚集地提供技术支持 | <a href="https://dngamer.site/" target="_blank">DN聚集地</a></p>
</div>
"""

# Gradio 界面
with gr.Blocks(theme="base",
               css=custom_css,
               title="DNre配装器",
               ) as demo:
    # gr.Markdown('# ![Logo](data/logo.ico) DN怀旧服 50级配装模拟器v0.1')
    with ms.Application():
        logo()

    job, save_btn, load_btn, save_file, load_file = create_main_tab()

    # 装备页
    equipment_list = create_equipment_tab()
    # 纹章页
    glyph_base, glyph_plus = create_glyph_tab()
    # 卡片页
    card_skill_list, card_list = create_card_tab()
    # 石板页
    rune_list = create_rune_tab()
    # 时装页
    skin_list = create_skin_tab()
    # 综合等级页
    surplus_list = create_surplus_level_tab()
    # 其他页
    other_list = create_others_tab()
    # 属性分析页
    dps_list = create_dps_tab()

    all_input = [job] + \
                equipment_list + \
                glyph_base + glyph_plus + \
                rune_list + \
                skin_list + \
                surplus_list + \
                other_list + \
                dps_list + \
                card_skill_list + card_list

    with gr.Row():
        submit_btn = gr.Button("计算面板", variant="primary")
    gr.Markdown("---")
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
    gr.Markdown("---")
    gr.Markdown("### 面板计算结果")
    with gr.Row():
        out_text1 = gr.Textbox(label="基础信息")
        out_text2 = gr.Textbox(label="属性信息")
    with gr.Row():
        out_text3 = gr.Textbox(label="一般信息")
        out_text4 = gr.Textbox(label="特殊攻击信息")
    with gr.Row():
        out_text5 = gr.Textbox(label="属性攻击信息")
        out_text6 = gr.Textbox(label="属性防御信息")
    with gr.Row():
        out_text7 = gr.Textbox(label="特殊防御信息")
        out_text8 = gr.Textbox(label="其他信息")
    submit_btn.click(main_func, inputs=all_input, outputs=[out_text1, out_text2, out_text3, out_text4,
                                                           out_text5, out_text6, out_text7, out_text8,
                                                           dps_text, dps_increase_plot,
                                                           def_text, def_increase_plot,
                                                           magic_def_text, magic_def_increase_plot])
    save_btn.click(save_options, inputs=all_input, outputs=save_file)

    # 为了让加载配置对实时更新的选项生效，再跑一边，顺序反着是因为gradio的button顺序是反着触发的
    load_btn.click(load_options2, outputs=all_input)
    load_btn.click(load_options, inputs=load_file, outputs=all_input)

    job.change(update_all, inputs=[job], outputs=equipment_list[:7] + other_list[5:14] + dps_list[:15])

    demo.add(gr.HTML(custom_html))

if env_now == "exe":
    port_now = 7866
    print(f"\n\n如果配装器网页没有自动弹出，请手动打开网页: http://127.0.0.1:{port_now}\n"
          "配装器使用过程中请勿关闭此窗口！\n\n")
else:
    port_now = None

demo.launch(
    # server_name="0.0.0.0",
    server_port=port_now,
    favicon_path=get_my_path("data/logo2.ico"),
    max_file_size="10kb",
    show_api=False,
    share=False,
    inbrowser=True)
