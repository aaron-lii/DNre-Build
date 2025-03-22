"""
计算基础属性
"""
import json
import gradio as gr

from src.tool_func import job_info_dict2, get_my_path

with open(get_my_path('data/player_base.json'), 'r', encoding='utf-8') as file:
    player_base_state_json = json.load(file)


def player_base_func(job):
    if job not in job_info_dict2:
        gr.Warning("请选择职业")
    return player_base_state_json["50"][job]


