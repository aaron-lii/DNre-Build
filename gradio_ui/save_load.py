"""
用于保存配装和加载配装
"""
import os
import uuid
from datetime import datetime
import gradio as gr
import time


load_data = []

def save_options(*args):
    """ 保存配置文件 """
    random_id = uuid.uuid4()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    job_now = args[0]

    save_dir = f"tmp_saves/{random_id}"
    os.mkdir(save_dir)
    save_path = f"tmp_saves/{random_id}/{job_now}{formatted_date}.txt"

    with open(save_path, "w") as f_w:
        f_w.write(str(args))

    return save_path


def load_options(input_file_path):
    """ 加载配置文件 """
    global load_data
    if not input_file_path:
        raise gr.Error("未上传配置文件")
    print(input_file_path)
    load_data = []
    with open(input_file_path, "r") as f_r:
        for line in f_r.readlines():
            try:
                load_data = eval(line.strip())
            except Exception as e:
                print(e)
                gr.Warning("加载配置文件出错")
    if len(load_data) == 0:
        raise gr.Error("加载配置文件出错")

    res_val = []
    for i in range(len(load_data)):
        res_val.append(gr.update(value=load_data[i]))

    return res_val


def load_options2():
    """ 二次加载配置文件 """
    global load_data
    # 不等待的话gradio来不及更新
    time.sleep(1)

    return load_data

