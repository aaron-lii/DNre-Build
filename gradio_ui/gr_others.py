"""
其他属性
"""
import json
import gradio as gr

from src.tool_func import get_my_path


def get_appellation_data():
    """ 获取appellation数据 """
    with open(get_my_path('data/appellation.json'), 'r', encoding='utf-8') as file:
        appellation_dict = json.load(file)
    return appellation_dict


def get_skill_data():
    """ 获取skill数据 """
    with open(get_my_path('data/skill.json'), 'r', encoding='utf-8') as file:
        skill_dict = json.load(file)
    return skill_dict


# 直接创建实例
appellation_dict = get_appellation_data()
skill_dict = get_skill_data()


def get_team_skill_options():
    """ 生成团队buff列表 """
    res_list = []
    for _ in range(8):
        res_list.append([0, "无"])

    skill_list_now = list(skill_dict["团队buff"].keys())
    for i in range(len(skill_list_now)):
        skill_name_now = skill_list_now[i]
        skill_state_name1 = list(skill_dict["团队buff"][skill_name_now].keys())[0]
        skill_max_now = len(skill_dict["团队buff"][skill_name_now][skill_state_name1])
        res_list[i] = [skill_max_now, skill_name_now]

    return res_list


def get_association_skill_options():
    """ 生成公会buff列表 """
    res_list = []
    for _ in range(4):
        res_list.append([0, "无"])

    skill_list_now = list(skill_dict["公会buff"].keys())
    for i in range(len(skill_list_now)):
        skill_name_now = skill_list_now[i]
        skill_state_name1 = list(skill_dict["公会buff"][skill_name_now].keys())[0]
        skill_max_now = len(skill_dict["公会buff"][skill_name_now][skill_state_name1])
        res_list[i] = [skill_max_now, skill_name_now]

    return res_list


def update_skill_options(job):
    """ 根据job的选择更新选项 """
    res_list = []
    for _ in range(9):
        res_list.append(gr.update(maximum=0, value=0, label="无"))

    # 更新被动
    if job in skill_dict["被动"]:
        skill_list_now = list(skill_dict["被动"][job].keys())
        for i in range(len(skill_list_now)):
            skill_state_name1 = list(skill_dict["被动"][job][skill_list_now[i]].keys())[0]
            skill_max_now = len(skill_dict["被动"][job][skill_list_now[i]][skill_state_name1])
            res_list[i] = gr.update(maximum=skill_max_now, label=skill_list_now[i], value=0)

    # 更新个人buff
    if job in skill_dict["个人buff"]:
        skill_list_now = list(skill_dict["个人buff"][job].keys())
        for i in range(len(skill_list_now)):
            skill_state_name1 = list(skill_dict["个人buff"][job][skill_list_now[i]].keys())[0]
            skill_max_now = len(skill_dict["个人buff"][job][skill_list_now[i]][skill_state_name1])
            res_list[5 + i] = gr.update(maximum=skill_max_now, label=skill_list_now[i], value=0)
    return res_list


def update_appellation_options(appellation_input):
    """ 根据appellation选择更新文本框 """
    if appellation_input == "无":
        return gr.update(value="无")
    appellation_state = appellation_dict[appellation_input]
    appellation_info = ""
    for key, val in appellation_state.items():
        appellation_info += key + ": " + str(val) + "\n"
    return gr.update(value=appellation_info.strip())


def create_others_tab():
    # 称号list
    appellation_list = ["无"] + list(appellation_dict.keys())
    # 通用技能list
    base_skill_list = list(skill_dict["被动"]["通用"].keys())
    base_skill_lv_max_list = []
    for skill_name_now in base_skill_list:
        base_skill_state_name1 = list(skill_dict["被动"]["通用"][skill_name_now].keys())[0]
        base_skill_lv_max_list.append(len(skill_dict["被动"]["通用"][skill_name_now][base_skill_state_name1]))
    # 团队buff list
    team_skill_list = get_team_skill_options()
    # 公会buff list
    association_skill_list = get_association_skill_options()

    with gr.Tab("其他属性"):
        gr.Markdown("### 称号")
        with gr.Row():
            appellation = gr.Dropdown(appellation_list, label="称号")
            appellation_info = gr.TextArea(value="无", label="称号属性预览", lines=4)
        gr.Markdown("### 时装收集")
        with gr.Row():
            skin_collections = gr.Slider(minimum=0, maximum=50, value=0, step=1, label="时装收集数量")
        gr.Markdown("---")
        gr.Markdown("### 被动技能")
        with gr.Row():
            skill1 = gr.Slider(minimum=0, maximum=base_skill_lv_max_list[0],
                               value=0, step=1, label=base_skill_list[0])
            skill2 = gr.Slider(minimum=0, maximum=base_skill_lv_max_list[1],
                               value=0, step=1, label=base_skill_list[1])
            skill3 = gr.Slider(minimum=0, maximum=base_skill_lv_max_list[2],
                               value=0, step=1, label=base_skill_list[2])
            skill4 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
        with gr.Row():
            skill5 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            skill6 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            skill7 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            skill8 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
        gr.Markdown("### 个人buff")
        with gr.Row():
            personal_skill1 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            personal_skill2 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            personal_skill3 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
            personal_skill4 = gr.Slider(minimum=0, maximum=0, value=0, step=1, label="无")
        gr.Markdown("### 团队buff")
        with gr.Row():
            team_skill1 = gr.Slider(minimum=0, maximum=team_skill_list[0][0],
                                    value=0, step=1, label=team_skill_list[0][1])
            team_skill2 = gr.Slider(minimum=0, maximum=team_skill_list[1][0],
                                    value=0, step=1, label=team_skill_list[1][1])
            team_skill3 = gr.Slider(minimum=0, maximum=team_skill_list[2][0],
                                    value=0, step=1, label=team_skill_list[2][1])
            team_skill4 = gr.Slider(minimum=0, maximum=team_skill_list[3][0],
                                    value=0, step=1, label=team_skill_list[3][1])
        with gr.Row():
            team_skill5 = gr.Slider(minimum=0, maximum=team_skill_list[4][0],
                                    value=0, step=1, label=team_skill_list[4][1])
            team_skill6 = gr.Slider(minimum=0, maximum=team_skill_list[5][0],
                                    value=0, step=1, label=team_skill_list[5][1])
            team_skill7 = gr.Slider(minimum=0, maximum=team_skill_list[6][0],
                                    value=0, step=1, label=team_skill_list[6][1])
            team_skill8 = gr.Slider(minimum=0, maximum=team_skill_list[7][0],
                                    value=0, step=1, label=team_skill_list[7][1])
        gr.Markdown("### 公会buff")
        with gr.Row():
            association_skill1 = gr.Slider(minimum=0, maximum=association_skill_list[0][0],
                                           value=0, step=1, label=association_skill_list[0][1])
            association_skill2 = gr.Slider(minimum=0, maximum=association_skill_list[1][0],
                                           value=0, step=1, label=association_skill_list[1][1])
            association_skill3 = gr.Slider(minimum=0, maximum=association_skill_list[2][0],
                                           value=0, step=1, label=association_skill_list[2][1])
            association_skill4 = gr.Slider(minimum=0, maximum=association_skill_list[3][0],
                                           value=0, step=1, label=association_skill_list[3][1])

    res_list = [appellation, skin_collections,
                skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8,
                personal_skill1, personal_skill2, personal_skill3, personal_skill4,
                team_skill1, team_skill2, team_skill3, team_skill4,
                team_skill5, team_skill6, team_skill7, team_skill8,
                association_skill1, association_skill2, association_skill3, association_skill4]

    appellation.change(update_appellation_options, inputs=[appellation], outputs=[appellation_info])

    return res_list
