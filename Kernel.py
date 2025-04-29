# 后端
import os
import traceback


# 字体
def setup_fonts(plt, fm):
    """设置中文字体"""
    try:
        # 先设置系统字体作为备用
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 检查并使用指定的字体
        local_font = "Text.ttf"
        if os.path.exists(local_font):
            font_path = local_font
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            fm.fontManager.addfont(font_path) # 注册本地字体

    except Exception as e:
        print(f"字体设置警告: {str(e)}")

def get_font_prop(fm):
    """获取字体的属性"""
    try:
        local_font = "Text.ttf" # 指定的字体
        if os.path.exists(local_font):
            return fm.FontProperties(fname=local_font)
        return fm.FontProperties(family='Microsoft YaHei') # 如果用户不小心删了字体再使用【微软雅黑】
    except:
        return fm.FontProperties()

import json

def read_config():
    """读取配置文件"""

    result_config = {
        "weather_info": {
            "province": "",
            "city": "",
            "county": ""
        },
        "health_info": {
            "age": "",
            "height": "",
            "weight": "",
            "steps": "",
            "sleep": ""
        }
    }

    if os.path.exists("history.json"):
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"配置文件格式错误，使用默认配置。")
            return result_config
        except Exception:
            print(traceback.format_exc())
    else:
        return result_config

    # 处理天气信息
    if "weather_info" in config and isinstance(config["weather_info"], dict):
        for key in result_config["weather_info"]:
            if key in config["weather_info"] and isinstance(config["weather_info"][key], str):
                result_config["weather_info"][key] = config["weather_info"][key]

    # 处理健康信息
    if "health_info" in config and isinstance(config["health_info"], dict):
        for key in result_config["health_info"]:
            if key in config["health_info"] and isinstance(config["health_info"][key], float):
                result_config["health_info"][key] = config["health_info"][key]

    return result_config

def save_config(config):
    """保存配置信息"""
    file_path = "history.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)