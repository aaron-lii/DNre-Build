"""
属性收益页面
"""

import json
import gradio as gr

from src.tool_func import get_my_path


def get_boss_data():
    """ 获取boss数据 """
    with open(get_my_path('data/boss.json'), 'r', encoding='utf-8') as file:
        boss_dict = json.load(file)
    return boss_dict


def get_dps_type_data():
    """ 获取职业默认输出属性 """
    with open(get_my_path('data/dps_type.json'), 'r', encoding='utf-8') as file:
        dps_type_dict = json.load(file)
    return dps_type_dict


# 直接构建实例
boss_dict = get_boss_data()
dps_type_dict = get_dps_type_data()


def update_dps_options(job):
    res = []
    for i in range(12):
        res.append(gr.update(value=dps_type_dict[job][i]))

    return res


def update_boss_options(boss_input):
    """ 根据boss选择更新文本框 """
    boss_state = boss_dict[boss_input]
    boss_info = ""
    for key, val in boss_state.items():
        boss_info += key + ": " + str(val) + "\n"
    return gr.update(value=boss_info.strip())


def create_dps_tab():
    boss_list = list(boss_dict.keys())

    with gr.Tab("战力分析"):
        gr.Markdown("""
        <span style="color:red; font-weight:bold;">战力标准仅供同职业、同技能构成、同boss情况下不同配装之间比较。
        使用战力分析默认您已理解本页面中的评判标准。</span>
        ### 计算公式
        战斗力=(面板x技能百分比+技能固伤)x(1+属性攻-属性抗)x(1+暴击率x(1-暴击抵抗率))x(1+最终伤害)x(1+其他增伤)
        
        生存力=HP/(1-防御百分比)/(1+boss暴击率x(1-暴击抵抗率))
        """)
        gr.Markdown("""
        ### 技能构成
        请选择按照物攻还是魔攻，哪种属性攻，对应技能的面板，作为配装强度的评判标准
        
        懒得想就保持默认的技能面板100%+0也行吧
        """)
        with gr.Row():
            atk_type1 = gr.Dropdown(["物攻", "魔攻"], label="物魔选择")
            atk_type2 = gr.Dropdown(["无", "光", "暗", "水", "火"], label="属性攻选择")
            atk_num1 = gr.Number(value=100, precision=0, label="技能百分比部分%")
            atk_num2 = gr.Number(value=0, precision=0, label="技能固定伤害部分")
        with gr.Row():
            atk_type3 = gr.Dropdown(["无", "物攻", "魔攻"], label="物魔选择")
            atk_type4 = gr.Dropdown(["无", "光", "暗", "水", "火"], label="属性攻选择")
            atk_num3 = gr.Number(value=0, precision=0, label="技能百分比部分%")
            atk_num4 = gr.Number(value=0, precision=0, label="技能固定伤害部分")
        with gr.Row():
            atk_type5 = gr.Dropdown(["无", "物攻", "魔攻"], label="物魔选择")
            atk_type6 = gr.Dropdown(["无", "光", "暗", "水", "火"], label="属性攻选择")
            atk_num5 = gr.Number(value=0, precision=0, label="技能百分比部分%")
            atk_num6 = gr.Number(value=0, precision=0, label="技能固定伤害部分")

        gr.Markdown("""
        ### 目标BOSS
        不同boss抗性不同，属性收益也不同
        """)
        with gr.Row():
            target_boss = gr.Dropdown(boss_list, label="BOSS选择")
            boss_state = gr.TextArea(label="BOSS属性预览", lines=4)

    res_list = [atk_type1, atk_type2, atk_num1, atk_num2,
                atk_type3, atk_type4, atk_num3, atk_num4,
                atk_type5, atk_type6, atk_num5, atk_num6,
                target_boss]

    target_boss.change(update_boss_options, inputs=[target_boss], outputs=[boss_state])

    return res_list
