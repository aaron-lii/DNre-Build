"""
计算基础属性
"""
import gradio as gr

from src.tool_func import job_info_dict2, player_base_state_json


def player_base_func(job):
    if job not in job_info_dict2:
        gr.Warning("请选择职业")
    return player_base_state_json["50"][job]
