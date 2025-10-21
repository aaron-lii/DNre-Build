"""
计算基础属性
"""
import gradio as gr

from src.tool_func import job_info_dict2, player_base_state_json


def player_base_func(job, level: str = "50"):
    if job not in job_info_dict2:
        gr.Warning("请选择职业")
    if level not in player_base_state_json:
        try:
            level = sorted(player_base_state_json.keys(), key=lambda x: int(x))[-1]
        except Exception:
            level = "50"
    return player_base_state_json[level][job]
