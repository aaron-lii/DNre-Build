"""
主页
"""

import gradio as gr


def create_main_tab():
    with gr.Tab("主页"):
        text_info = """
        <span style="color:red; font-weight:bold;">内测中，随时可能因为作者更新而暂时打不开页面</span>
        ### 使用说明
        1. 在本页面选择角色职业
        2. 在装备页、纹章页、石板页、时装页、综合等级页、其他属性页面选择对应装备
        4. 如果选项太多，可以直接框内打字搜索
        6. 点击页面下方【计算面板】按钮
        
        ### 保存与加载配装
        各种装备选项太多，建议配完一套后保存配装，方便以后微调
        1. 保存配装: 将你勾选的配装方案保存成文件并下载
        2. 加载配装: 上传配装文件并加载
        
        ### 备注
        1. MP恢复、移速、硬直眩晕抵抗计算异常
        2. 如有需要的职业buff、称号、装备、附魔未收录的，请联系作者
        
        **当前数据版本**: 2025-3-11；**作者**: MXX；**数据支持**: 阿笑
        """
        jobs_list = ["请选择你的职业",
                     "剑皇", "月之领主", "狂战士", "毁灭者",
                     "狙翎", "魔羽", "影舞者", "风行者",
                     "火舞", "冰灵", "时空领主", "黑暗女王",
                     "圣骑士", "十字军", "圣徒", "雷神",
                     "重炮手", "机械大师", "炼金圣士", "药剂师"]
        with gr.Row():
            gr.Markdown(text_info)
        with gr.Row():
            job = gr.Dropdown(jobs_list, label="职业")
        with gr.Row():
            save_btn = gr.Button("保存配装", variant="secondary")
            load_btn = gr.Button("加载配装", variant="secondary")
        with gr.Row():
            file_output = gr.File(label="下载配装文件", interactive=False)
            file_input = gr.File(label="上传配装文件")

    return job, save_btn, load_btn, file_output, file_input
