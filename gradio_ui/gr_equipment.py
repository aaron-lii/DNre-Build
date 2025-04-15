"""
equipment
"""
import json
import gradio as gr

from src.tool_func import get_my_path


def get_base_data():
    """ 获取base数据 """
    base_dict = {}
    # 打开 JSON 文件
    with open(get_my_path('data/equipment_base.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for job, val in data.items():
            if job not in base_dict:
                base_dict[job] = {}
            for lv, val2 in val.items():
                for equipment_name, val3 in val2.items():
                    part = val3["部位"]
                    if "-" in part:
                        part = part.split("-", 1)[0]
                    if part not in base_dict[job]:
                        base_dict[job][part] = []
                    base_dict[job][part].append(lv + "-" + equipment_name)
    return base_dict


def get_jewelry_data():
    """ 获取jewelry数据 """
    jewelry_dict = {}
    # 打开 JSON 文件
    with open(get_my_path('data/jewelry.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for part, val1 in data.items():
            if part not in jewelry_dict:
                jewelry_dict[part] = {}
            for lv, val2 in val1.items():
                for jewelry_name, val3 in val2.items():
                    name_now = lv + "-" + jewelry_name
                    state_list = []
                    for state_i, val4 in val3["属性"].items():
                        state_list.append(str(state_i) + ": " + str(val4))
                    jewelry_dict[part][name_now] = state_list

    return jewelry_dict


# 这里直接构建实例
equipment_base_dict = get_base_data()
jewelry_dict = get_jewelry_data()


def get_enchant_data():
    """ 获取enchant数据 """
    enchant_dict = {}
    with open(get_my_path('data/equipment_enchant.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for type1, val1 in data.items():
            if type1 not in enchant_dict:
                enchant_dict[type1] = []
            for name2, val2 in val1.items():
                enchant_dict[type1].append(name2)

    return enchant_dict


def get_suffix_data():
    """ 获取suffix数据 """
    suffix_dict = {}
    with open(get_my_path('data/equipment_suffix.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)

    for part, val in equipment_base_dict["战士"].items():
        for equipment_now in val:
            lv, equipment_name = equipment_now.split("-", 1)
            if lv == "50S":
                if part not in suffix_dict:
                    suffix_dict[part] = {}
                suffix_dict[part] = list(data["战士"][lv][equipment_name].keys())
                break

    return suffix_dict


def update_equipment_options(job):
    """ 根据job的选择更新选项 """
    job_info_dict = {"剑圣": "战士", "战神": "战士", "箭神": "弓箭", "游侠": "弓箭",
                     "元素": "法师", "魔导": "法师", "祭司": "牧师", "贤者": "牧师",
                     "工程": "学者", "炼金": "学者"}
    job_info_dict2 = {"剑皇": "剑圣", "月之领主": "剑圣", "狂战士": "战神", "毁灭者": "战神",
                      "狙翎": "箭神", "魔羽": "箭神", "影舞者": "游侠", "风行者": "游侠",
                      "火舞": "元素", "冰灵": "元素", "时空领主": "魔导", "黑暗女王": "魔导",
                      "圣骑士": "贤者", "十字军": "贤者", "圣徒": "祭司", "雷神": "祭司",
                      "重炮手": "工程", "机械大师": "工程", "炼金圣士": "炼金", "药剂师": "炼金"}
    star_pre = "40S-海龙"

    job_one = job_info_dict2[job]
    base_job = job_info_dict[job_one]
    choice_lists = []
    for part in ["主手", "副手", "头盔", "上装", "下装", "手套", "鞋子"]:
        star_equipment_list = []
        for equipment_name in equipment_base_dict[base_job][part]:
            if star_pre in equipment_name:
                star_equipment_list += [equipment_name + "★", equipment_name + "★★", equipment_name + "★★★"]

        choice_lists.append(["无"] + sorted(star_equipment_list +
                                           equipment_base_dict[job_one][part] +
                                           equipment_base_dict[base_job][part]))

    res_list = [gr.update(choices=choice_lists[0]),
                gr.update(choices=choice_lists[1]),
                gr.update(choices=choice_lists[2]),
                gr.update(choices=choice_lists[3]),
                gr.update(choices=choice_lists[4]),
                gr.update(choices=choice_lists[5]),
                gr.update(choices=choice_lists[6]),
                ]

    return res_list


def update_jewelry_options(jewelry_input):
    """ 根据jewelry更新随机属性选项 """
    for part, val in jewelry_dict.items():
        if jewelry_input in val:
            res_list = val[jewelry_input]
            return gr.update(choices=res_list, value=res_list[0])


def create_equipment_tab():
    list_tmp = ["无"]
    enchant_dict = get_enchant_data()
    suffix_dict = get_suffix_data()
    atk_en_list = sorted(enchant_dict["atk_enchant"] + enchant_dict["base_enchant"], reverse=True)
    def_en_list = sorted(enchant_dict["def_enchant"] + enchant_dict["base_enchant"])
    ring_list = ["无"] + sorted(list(jewelry_dict["戒指"].keys()))
    necklace_list = ["无"] + sorted(list(jewelry_dict["项链"].keys()))
    earrings_list = ["无"] + sorted(list(jewelry_dict["耳环"].keys()))

    with gr.Tab("装备页"):
        gr.Markdown("### 武器和防具")
        with gr.Row():
            with gr.Column():
                weapon1 = gr.Dropdown(list_tmp, label="主手武器")
                weapon1_suffix = gr.Dropdown(suffix_dict["主手"], label="主手武器后缀")
                weapon1_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="主手武器强化")
                # weapon1_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="主手武器升星")
            with gr.Column():
                weapon1_enchant = gr.Dropdown(atk_en_list, label="主手武器附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                weapon2 = gr.Dropdown(list_tmp, label="副手武器")
                weapon2_suffix = gr.Dropdown(suffix_dict["副手"], label="副手武器后缀")
                weapon2_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="副手武器强化")
                # weapon2_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="副手武器升星")
            with gr.Column():
                weapon2_enchant = gr.Dropdown(atk_en_list, label="副手武器附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                hat = gr.Dropdown(list_tmp, label="头盔")
                hat_suffix = gr.Dropdown(suffix_dict["头盔"], label="头盔后缀")
                hat_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="头盔强化")
                # hat_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="头盔升星")
            with gr.Column():
                hat_enchant = gr.Dropdown(def_en_list, label="头盔附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                cloths = gr.Dropdown(list_tmp, label="上装")
                cloths_suffix = gr.Dropdown(suffix_dict["上装"], label="上装后缀")
                cloths_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="上装强化")
                # cloths_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="上装升星")
            with gr.Column():
                cloths_enchant = gr.Dropdown(def_en_list, label="上装附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                trousers = gr.Dropdown(list_tmp, label="下装")
                trousers_suffix = gr.Dropdown(suffix_dict["下装"], label="下装后缀")
                trousers_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="下装强化")
                # trousers_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="下装升星")
            with gr.Column():
                trousers_enchant = gr.Dropdown(def_en_list, label="下装附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                gloves = gr.Dropdown(list_tmp, label="手套")
                gloves_suffix = gr.Dropdown(suffix_dict["手套"], label="手套后缀")
                gloves_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="手套强化")
                # gloves_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="手套升星")
            with gr.Column():
                gloves_enchant = gr.Dropdown(def_en_list, label="手套附魔", multiselect=True)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                shoes = gr.Dropdown(list_tmp, label="鞋子")
                shoes_suffix = gr.Dropdown(suffix_dict["鞋子"], label="鞋子后缀")
                shoes_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="鞋子强化")
                # shoes_star = gr.Slider(minimum=0, maximum=3, value=0, step=1, label="鞋子升星")
            with gr.Column():
                shoes_enchant = gr.Dropdown(def_en_list, label="鞋子附魔", multiselect=True)

        gr.Markdown("---")
        gr.Markdown("### 首饰")
        with gr.Row():
            ring1 = gr.Dropdown(ring_list, label="戒指1")
            ring1_state = gr.Dropdown(list_tmp, label="戒指1随机属性")
            ring1_enchant = gr.Dropdown(atk_en_list, label="戒指1附魔", multiselect=True)
        with gr.Row():
            ring2 = gr.Dropdown(ring_list, label="戒指2")
            ring2_state = gr.Dropdown(list_tmp, label="戒指2随机属性")
            ring2_enchant = gr.Dropdown(atk_en_list, label="戒指2附魔", multiselect=True)
        with gr.Row():
            necklace = gr.Dropdown(necklace_list, label="项链")
            necklace_state = gr.Dropdown(list_tmp, label="项链随机属性")
            necklace_enchant = gr.Dropdown(def_en_list, label="项链附魔", multiselect=True)
        with gr.Row():
            earrings = gr.Dropdown(earrings_list, label="耳环")
            earrings_state = gr.Dropdown(list_tmp, label="耳环随机属性")
            earrings_enchant = gr.Dropdown(def_en_list, label="耳环附魔", multiselect=True)

    equipment_list = [weapon1, weapon2, hat, cloths, trousers, gloves, shoes]
    equipment_suffix_list = [weapon1_suffix, weapon2_suffix, hat_suffix, cloths_suffix,
                             trousers_suffix, gloves_suffix, shoes_suffix]
    equipment_grade_list = [weapon1_grade, weapon2_grade, hat_grade, cloths_grade,
                            trousers_grade, gloves_grade, shoes_grade]
    # equipment_star_list = [weapon1_star, weapon2_star, hat_star, cloths_star,
    #                        trousers_star, gloves_star, shoes_star]
    equipment_enchant_list = [weapon1_enchant, weapon2_enchant, hat_enchant, cloths_enchant,
                              trousers_enchant, gloves_enchant, shoes_enchant]
    jewelry_list = [ring1, ring2, necklace, earrings]
    jewelry_state_list = [ring1_state, ring2_state, necklace_state, earrings_state]
    jewelry_enchant_list = [ring1_enchant, ring2_enchant, necklace_enchant, earrings_enchant]

    # 实时更新首饰随机属性
    ring1.change(update_jewelry_options, inputs=[ring1], outputs=[ring1_state])
    ring2.change(update_jewelry_options, inputs=[ring2], outputs=[ring2_state])
    necklace.change(update_jewelry_options, inputs=[necklace], outputs=[necklace_state])
    earrings.change(update_jewelry_options, inputs=[earrings], outputs=[earrings_state])

    return equipment_list + equipment_suffix_list + equipment_grade_list + \
           equipment_enchant_list + \
           jewelry_list + jewelry_state_list + jewelry_enchant_list
