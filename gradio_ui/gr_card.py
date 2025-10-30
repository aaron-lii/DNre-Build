"""
卡片页
"""

import gradio as gr

from src.tool_func import card_skill_json, card_json


def get_card_data():
    """ 获取卡片数据 """
    card_skill_list = list(card_skill_json.keys())
    card_list = list(card_json.keys())
    return card_skill_list, card_list


def create_card_tab():
    """ gr页面 (动态技能与卡片数量) """
    card_skill_list, card_list = get_card_data()

    card_skill_res_list = []
    card_res_list = []

    with gr.Tab("卡片页"):
        gr.Markdown("### 掌握之力")
        for i in range(len(card_skill_list) // 4):
            with gr.Row():
                for j in range(4):
                    card_skill_levle_now = gr.Slider(minimum=0, maximum=20, value=0, step=1,
                                                     label=card_skill_list[i * 4 + j])
                    card_skill_res_list.append(card_skill_levle_now)

        gr.Markdown("---")
        # 每页16张卡 (4x4), 页数动态
        import math
        cards_per_page = 16
        total_pages = math.ceil(len(card_list) / cards_per_page)
        for page in range(total_pages):
            gr.Markdown(f"### 怪物卡片 第{page + 1}页")
            page_cards = card_list[page * cards_per_page: (page + 1) * cards_per_page]
            # 4 行，每行最多4列
            for row_start in range(0, len(page_cards), 4):
                with gr.Row():
                    for idx in range(row_start, min(row_start + 4, len(page_cards))):
                        card_now = gr.Radio(choices=["无", "C", "B", "A", "S", "L"],
                                            label=page_cards[idx],
                                            value="无")
                        card_res_list.append(card_now)

    return card_skill_res_list, card_res_list
