"""
equipment
"""
import gradio as gr

from src.tool_func import equipment_base_json, jewelry_json, equipment_enchant_json, equipment_suffix_json, job_info_dict, job_info_dict2, equipment_grade_json

job_now_list = ["无", "无", "无"]


def get_base_data():
    """ 获取base数据 """
    base_dict = {}
    data = equipment_base_json
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
    return base_dict, data


def get_jewelry_data():
    """ 获取jewelry数据 """
    jewelry_dict = {}
    data = jewelry_json
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
equipment_base_dict, equipment_ori_dict = get_base_data()
jewelry_dict = get_jewelry_data()


def get_enchant_data():
    """ 获取enchant数据 """
    enchant_dict = {}
    data = equipment_enchant_json
    for type1, val1 in data.items():
        if type1 not in enchant_dict:
            enchant_dict[type1] = []
        for name2, val2 in val1.items():
            enchant_dict[type1].append(name2)

    return enchant_dict


def get_suffix_data():
    """ 获取suffix数据 """
    suffix_dict = {}
    data = equipment_suffix_json

    for part, val in equipment_base_dict["战士"].items():
        for equipment_now in val:
            lv, equipment_name = equipment_now.split("-", 1)
            if lv == "50S":
                if part not in suffix_dict:
                    suffix_dict[part] = {}
                suffix_dict[part] = list(data["战士"][lv][equipment_name].keys())
                break

    return suffix_dict, data


enchant_dict = get_enchant_data()
suffix_dict, suffix_ori_dict = get_suffix_data()


def update_equipment_options(job):
    """ 根据job的选择更新选项 """
    star_pre = "40S-海龙"

    mid_job = job_info_dict2[job]          # 中阶职业
    base_job = job_info_dict[mid_job]      # 基础职业
    global job_now_list
    # 保存: 高阶, 中阶, 基础
    job_now_list = [job, mid_job, base_job]

    choice_lists = []
    for part in ["主手", "副手", "头盔", "上装", "下装", "手套", "鞋子"]:
        star_equipment_list = []
        for equipment_name in equipment_base_dict[base_job][part]:
            if star_pre in equipment_name:
                star_equipment_list += [equipment_name + "★", equipment_name + "★★", equipment_name + "★★★"]

        choice_lists.append(["无"] + sorted(star_equipment_list +
                                           equipment_base_dict[mid_job][part] +
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


def update_single_equipment_display(equip_name: str, suffix_name: str, grade_num: int):
    """ 单件装备属性展示: 基础+后缀 以及 强化属性
    - 排除 '无'
    - 处理升星 (★) 对强化属性的加成
    - job 从全局 job_now_list 获取 (job_now_list[0] 高阶, job_now_list[1] 基础)
    """
    try:
        if equip_name in ["无", "", None] or suffix_name in [None, ""]:
            return gr.update(value="")
        high_job, mid_job, base_job = job_now_list  # 高阶 / 中阶 / 基础
        lv, equip_real_name = equip_name.split("-", 1)
        star_num = 0
        if "★" in equip_real_name:
            star_num = equip_real_name.count("★")
            equip_real_name = equip_real_name.replace("★", "")
        # 与计算逻辑保持一致: L装使用中阶职业, 非L装使用基础职业
        if "L" in lv:
            job_lookup = mid_job
        else:
            job_lookup = base_job
        # 基础属性
        state_base = equipment_base_json[job_lookup][lv][equip_real_name]["属性"]
        # 后缀属性
        state_suffix = equipment_suffix_json[job_lookup][lv][equip_real_name].get(suffix_name, {})
        # 合并基础+后缀
        base_plus_dict = {}
        for d in [state_base, state_suffix]:
            for k, v in d.items():
                if k in base_plus_dict:
                    if "%" in str(k):
                        base_plus_dict[k] += v
                    else:
                        base_plus_dict[k] += int(v)
                else:
                    base_plus_dict[k] = v
        # 强化属性
        grade_dict = {}
        if grade_num and grade_num > 0:
            grade_ori = equipment_grade_json[job_lookup][lv][equip_real_name][str(grade_num)]
            star_rate = 1 + star_num * 0.08
            for k, v in grade_ori.items():
                grade_dict[k] = v * star_rate
        # 格式化输出
        lines = []
        if base_plus_dict:
            lines.append("【基础+后缀】:")
            for k in sorted(base_plus_dict.keys()):
                v = base_plus_dict[k]
                if isinstance(v, float) and "%" not in k:
                    v_show = int(v)
                else:
                    v_show = v
                lines.append(f"{k}: {v_show}")
        if grade_dict:
            lines.append("\n【强化】:")
            for k in sorted(grade_dict.keys()):
                v = grade_dict[k]
                # 强化属性可能有小数, 四舍五入到整数 (非百分比)
                if isinstance(v, float) and "%" not in k:
                    v_show = int(round(v))
                else:
                    v_show = v
                lines.append(f"{k}: {v_show}")
        return gr.update(value="\n".join(lines))
    except Exception:
        # 出错不阻塞 UI
        return gr.update(value="")


def create_equipment_tab():
    list_tmp = ["无"]
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
                weapon1_enchant = gr.Dropdown(atk_en_list, label="主手武器附魔", multiselect=True)
            with gr.Column():
                weapon1_out = gr.TextArea(label="主手武器属性", lines=8, interactive=False)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                weapon2 = gr.Dropdown(list_tmp, label="副手武器")
                weapon2_suffix = gr.Dropdown(suffix_dict["副手"], label="副手武器后缀")
                weapon2_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="副手武器强化")
                weapon2_enchant = gr.Dropdown(atk_en_list, label="副手武器附魔", multiselect=True)
            with gr.Column():
                weapon2_out = gr.TextArea(label="副手武器属性", lines=8, interactive=False)
        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                hat = gr.Dropdown(list_tmp, label="头盔")
                hat_suffix = gr.Dropdown(suffix_dict["头盔"], label="头盔后缀")
                hat_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="头盔强化")
                hat_enchant = gr.Dropdown(def_en_list, label="头盔附魔", multiselect=True)
            with gr.Column():
                hat_out = gr.TextArea(label="头盔属性", lines=8, interactive=False)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                cloths = gr.Dropdown(list_tmp, label="上装")
                cloths_suffix = gr.Dropdown(suffix_dict["上装"], label="上装后缀")
                cloths_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="上装强化")
                cloths_enchant = gr.Dropdown(def_en_list, label="上装附魔", multiselect=True)
            with gr.Column():
                cloths_out = gr.TextArea(label="上装属性", lines=8, interactive=False)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                trousers = gr.Dropdown(list_tmp, label="下装")
                trousers_suffix = gr.Dropdown(suffix_dict["下装"], label="下装后缀")
                trousers_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="下装强化")
                trousers_enchant = gr.Dropdown(def_en_list, label="下装附魔", multiselect=True)
            with gr.Column():
                trousers_out = gr.TextArea(label="下装属性", lines=8, interactive=False)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                gloves = gr.Dropdown(list_tmp, label="手套")
                gloves_suffix = gr.Dropdown(suffix_dict["手套"], label="手套后缀")
                gloves_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="手套强化")
                gloves_enchant = gr.Dropdown(def_en_list, label="手套附魔", multiselect=True)
            with gr.Column():
                gloves_out = gr.TextArea(label="手套属性", lines=8, interactive=False)

        gr.Markdown("---")
        with gr.Row():
            with gr.Column():
                shoes = gr.Dropdown(list_tmp, label="鞋子")
                shoes_suffix = gr.Dropdown(suffix_dict["鞋子"], label="鞋子后缀")
                shoes_grade = gr.Slider(minimum=0, maximum=15, value=11, step=1, label="鞋子强化")
                shoes_enchant = gr.Dropdown(def_en_list, label="鞋子附魔", multiselect=True)
            with gr.Column():
                shoes_out = gr.TextArea(label="鞋子属性", lines=8, interactive=False)

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
    equipment_enchant_list = [weapon1_enchant, weapon2_enchant, hat_enchant, cloths_enchant,
                              trousers_enchant, gloves_enchant, shoes_enchant]
    # 展示输出不参与主计算, 不放进返回列表
    equipment_out_list = [weapon1_out, weapon2_out, hat_out, cloths_out, trousers_out, gloves_out, shoes_out]

    jewelry_list = [ring1, ring2, necklace, earrings]
    jewelry_state_list = [ring1_state, ring2_state, necklace_state, earrings_state]
    jewelry_enchant_list = [ring1_enchant, ring2_enchant, necklace_enchant, earrings_enchant]

    # 实时更新首饰随机属性
    ring1.change(update_jewelry_options, inputs=[ring1], outputs=[ring1_state])
    ring2.change(update_jewelry_options, inputs=[ring2], outputs=[ring2_state])
    necklace.change(update_jewelry_options, inputs=[necklace], outputs=[necklace_state])
    earrings.change(update_jewelry_options, inputs=[earrings], outputs=[earrings_state])

    # 实时更新装备属性展示 (名称/后缀/强化变化均触发)
    for comp_name, comp_suffix, comp_grade, comp_out in zip(equipment_list, equipment_suffix_list, equipment_grade_list, equipment_out_list):
        comp_name.change(update_single_equipment_display, inputs=[comp_name, comp_suffix, comp_grade], outputs=[comp_out])
        comp_suffix.change(update_single_equipment_display, inputs=[comp_name, comp_suffix, comp_grade], outputs=[comp_out])
        comp_grade.change(update_single_equipment_display, inputs=[comp_name, comp_suffix, comp_grade], outputs=[comp_out])

    return equipment_list + equipment_suffix_list + equipment_grade_list + \
           equipment_enchant_list + \
           jewelry_list + jewelry_state_list + jewelry_enchant_list
