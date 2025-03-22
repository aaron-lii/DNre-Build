"""
skin页
"""

import gradio as gr
import json

from src.tool_func import get_my_path


def get_skin_data():
    """ 获取时装数据 """
    weapon1_skin_list = ["无"]
    weapon2_skin_list = ["无"]
    wing_skin_list = ["无"]
    tail_skin_list = ["无"]
    printing_skin_list = ["无"]
    necklace_skin_list = ["无"]
    earrings_skin_list = ["无"]
    ring_skin_list = ["无"]

    # 打开 JSON 文件
    with open(get_my_path('data/skin.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for key, val in data["weapon1_skin"].items():
            weapon1_skin_list.append(key)
        for key, val in data["weapon2_skin"].items():
            weapon2_skin_list.append(key)
        for key, val in data["wing_skin"].items():
            wing_skin_list.append(key)
        for key, val in data["tail_skin"].items():
            tail_skin_list.append(key)
        for key, val in data["printing_skin"].items():
            printing_skin_list.append(key)
        for key, val in data["necklace_skin"].items():
            necklace_skin_list.append(key)
        for key, val in data["earrings_skin"].items():
            earrings_skin_list.append(key)
        for key, val in data["ring_skin"].items():
            ring_skin_list.append(key)

    return [weapon1_skin_list, weapon2_skin_list, wing_skin_list,
            tail_skin_list, printing_skin_list, necklace_skin_list,
            earrings_skin_list, ring_skin_list]


def create_skin_tab():
    [weapon1_skin_list, weapon2_skin_list, wing_skin_list,
     tail_skin_list, printing_skin_list, necklace_skin_list,
     earrings_skin_list, ring_skin_list] = get_skin_data()

    with gr.Tab("时装页"):
        gr.Markdown("### 五件套")
        with gr.Row():
            with gr.Column():
                weapon1_skin = gr.Dropdown(weapon1_skin_list, label="主手")
                weapon2_skin = gr.Dropdown(weapon2_skin_list, label="副手")
            with gr.Column():
                wing_skin = gr.Dropdown(wing_skin_list, label="翅膀")
                printing_skin = gr.Dropdown(printing_skin_list, label="印花")
                tail_skin = gr.Dropdown(tail_skin_list, label="尾巴")
        gr.Markdown("---")
        gr.Markdown("### 首饰")
        with gr.Row():
            with gr.Column():
                necklace_skin = gr.Dropdown(necklace_skin_list, label="项链")
                earrings_skin = gr.Dropdown(earrings_skin_list, label="耳环")
            with gr.Column():
                ring1_skin = gr.Dropdown(ring_skin_list, label="戒指1")
                ring2_skin = gr.Dropdown(ring_skin_list, label="戒指2")

    return [weapon1_skin, weapon2_skin,
            wing_skin, tail_skin, printing_skin,
            necklace_skin, earrings_skin, ring1_skin, ring2_skin]
