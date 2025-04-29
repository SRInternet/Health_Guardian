"""
Health Guardian - 智能健康守护者

版本: 1.0
许可证: MIT License  
作者: 龚梓涵  
仓库地址: https://github.com/SRInternet/Health_Guardian
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import font_manager as fm
import sys, os
# from numpy.lib.histograms import histogram

from Kernel import * # 导入后端

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class HealthGuardian:
    WEATHER_API = "https://wis.qq.com/weather/common" # 天气 API （腾讯）

    def __init__(self, master):
        """初始化健康智能守护者"""
        self.history = {} #历史记录和当前数据的存档

        # 基本控件的定义
        self.county_entry = None
        self.weather_label = None
        self.city_entry = None
        self.province_entry = None
        self.steps_entry = None
        self.sleep_entry = None
        self.weight_entry = None
        self.height_entry = None
        self.age_entry = None

        # 前端
        self.master = master
        master.title("计算你的健康信息")
        master.iconphoto(True, tk.PhotoImage(file='UI.png'))
        self.create_ui()
        self.weather_data = None
        self.user_data = {}
        
        # 配置字体
        setup_fonts(plt=plt, fm=fm)

    def create_ui(self):
        """前端"""
        main_frame = ttk.Frame(self.master, padding=15)
        main_frame.pack(fill='both', expand=True)
        self.history = read_config()
        health_info = self.history['health_info']
        weather_info = self.history['weather_info']

        # 健康数据输入
        input_frame = ttk.LabelFrame(main_frame, text="个人信息", padding=10)
        input_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ttk.Label(input_frame, text="年龄:").grid(row=0, column=0, sticky='e')
        self.age_entry = ttk.Entry(input_frame)
        self.age_entry.insert(0, health_info['age'])
        self.age_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="身高(cm):").grid(row=1, column=0, sticky='e')
        self.height_entry = ttk.Entry(input_frame)
        self.height_entry.insert(0, health_info['height'])
        self.height_entry.grid(row=1, column=1)

        ttk.Label(input_frame, text="体重(kg):").grid(row=2, column=0, sticky='e')
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.insert(0, health_info['weight'])
        self.weight_entry.grid(row=2, column=1)

        ttk.Label(input_frame, text="每日步数:").grid(row=3, column=0, sticky='e')
        self.steps_entry = ttk.Entry(input_frame)
        self.steps_entry.insert(0, health_info['steps'])
        self.steps_entry.grid(row=3, column=1)

        ttk.Label(input_frame, text="睡眠时间(h):").grid(row=4, column=0, sticky='e')
        self.sleep_entry = ttk.Entry(input_frame)
        self.sleep_entry.insert(0, health_info['sleep'])
        self.sleep_entry.grid(row=4, column=1)

        # 天气输入
        weather_frame = ttk.LabelFrame(main_frame, text="位置信息", padding=10)
        weather_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        ttk.Label(weather_frame, text="省份:").grid(row=0, column=0, sticky='e')
        self.province_entry = ttk.Entry(weather_frame)
        self.province_entry.insert(0, weather_info['province'])
        self.province_entry.grid(row=0, column=1)

        ttk.Label(weather_frame, text="城市:").grid(row=1, column=0, sticky='e')
        self.city_entry = ttk.Entry(weather_frame)
        self.city_entry.insert(0, weather_info['city'])
        self.city_entry.grid(row=1, column=1)

        ttk.Label(weather_frame, text="区县:").grid(row=2, column=0, sticky='e')
        self.county_entry = ttk.Entry(weather_frame)
        self.county_entry.insert(0, weather_info['county'])
        self.county_entry.grid(row=2, column=1)

        # 天气显示区域
        self.weather_label = ttk.Label(main_frame, text="当前天气：未获取")
        self.weather_label.grid(row=1, column=0, columnspan=2, pady=10)

        # 控制按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # 关联点击事件
        ttk.Button(btn_frame, text="获取天气", command=self.get_weather).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="健康分析", command=self.analyze_health).pack(side='left', padx=5)


    def get_weather(self):
        """使用API获取天气"""
        self.master.title("请等待，正在响应……")
        self.history['weather_info'] = {
            'province': self.province_entry.get(),
            'city': self.city_entry.get(),
            'county': self.county_entry.get()}

        params = {
            'source': 'pc',
            'weather_type': 'observe',
            **self.history['weather_info']
        }

        # print(params)

        try:
            response = requests.get(self.WEATHER_API, params=params)
            data = response.json()

            if data['status'] != 200 or not data['data']['observe']:
                print(f"ValueError: {data}")
                raise ValueError("天气数据获取失败，请检查位置信息")

            self.weather_data = data['data']['observe']
            self.show_weather()

            save_config(self.history)
        except Exception as e:
            messagebox.showerror("错误", f"获取天气失败：{str(e)}") # 弹窗显示错误
            print(traceback.format_exc()) # 打印详细错误
        finally:
            self.master.title("计算你的健康信息")

    def show_weather(self):
        """显示天气信息"""
        if self.weather_data:
            weather_info = (
                f"当前天气：{self.weather_data['weather']}\n"
                f"温度：{self.weather_data['degree']}℃\n"
                f"湿度：{self.weather_data['humidity']}%\n"
                f"风力：{self.weather_data['wind_power']}级"
            )
            self.weather_label.config(text=weather_info)

    def collect_data(self):
        """收集并验证用户输入数据"""
        required_fields = {
            'age': self.age_entry.get(),
            'height': self.height_entry.get(),
            'weight': self.weight_entry.get(),
            'steps': self.steps_entry.get(),
            'sleep': self.sleep_entry.get()
        }

        for field, value in required_fields.items(): # 依次验证每个输入的有效性
            if not value:
                raise ValueError(f"请填写完整的 {field} 信息")

            try:
                if float(value) <= 0:
                    raise ValueError(f"无效的{field}数值")
                self.user_data[field] = float(value)
            except ValueError:
                raise ValueError(f"无效的{field}数值")

        self.history['health_info'] = self.user_data
        save_config(self.history)

    def analyze_health(self):
        """健康分析"""
        try:
            self.master.title("请等待，正在响应……")
            self.get_weather()
            self.collect_data()
            report = self.generate_report()
            self.visualize_data(report)
        except Exception as e:
            messagebox.showerror("输入错误", str(e))
            print(traceback.format_exc()) # 打印详细错误
        finally:
            self.master.title("计算你的健康信息")

    def generate_report(self):
        """生成完整健康报告"""
        return {
            'bmi': self.calculate_bmi(),
            'exercise': self.analyze_exercise(),
            'mental_health': self.assess_mental_health(),
            'weather_impact': self.analyze_weather_impact()
        }

    def calculate_bmi(self):
        """BMI计算与分类"""
        height = self.user_data['height'] / 100
        weight = self.user_data['weight']
        bmi = weight / (height ** 2)

        categories = [
            (18.5, "体重过轻"),
            (24, "健康体重"),
            (28, "超重"),
            (float('inf'), "肥胖")
        ] # 定义不同BMI对应的显示文字

        for limit, label in categories:
            if bmi <= limit:
                return {'value': round(bmi, 1), 'category': label}

    def analyze_exercise(self):
        """运动量分析"""
        steps = self.user_data['steps']
        if steps < 5000:
            return "建议增加日常活动量，每天至少步行5000步"
        elif 5000 <= steps < 10000:
            return "运动量良好，继续保持！"
        else:
            return "非常棒！您已达到推荐运动量"

    def assess_mental_health(self):
        """睡眠质量评估"""
        sleep_hours = self.user_data['sleep']
        if sleep_hours < 6:
            return "睡眠不足，建议增加休息时间"
        elif 6 <= sleep_hours <= 9:
            return "睡眠质量良好"
        else:
            return "注意保持规律的作息时间"

    def analyze_weather_impact(self):
        """天气影响分析"""
        if not self.weather_data:
            return "未获取天气数据"

        temp = float(self.weather_data['degree'])
        weather = self.weather_data['weather']

        advice = []
        if temp > 30:
            advice.append("注意防暑降温")
        elif temp < 10:
            advice.append("注意保暖防寒")

        if '雨' in weather:
            advice.append("雨天出行请注意安全")

        return "，".join(advice) if advice else "天气适宜户外活动"

    def visualize_data(self, report):
        """报告窗口"""

        # 创建报告窗口
        report_window = tk.Toplevel(self.master)
        report_window.title("健康分析报告")
        report_window.geometry("800x620")
        report_window.iconphoto(False, tk.PhotoImage(file='Dialog.png'))
        
        # 使用主题样式
        style = ttk.Style()
        style.configure('TNotebook', tabposition='n')
        style.configure('TNotebook.Tab', padding=[15,5], font=('Microsoft YaHei', 10))
        
        # 创建标签页容器
        notebook = ttk.Notebook(report_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        """概览标签页"""
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text='📊 概览')
        
        # 创建图表
        fig = plt.Figure(figsize=(8, 4), dpi=100, facecolor='#f8f9fa')
        ax = fig.add_subplot(111)
        
        metrics = ['BMI指数', '运动量', '睡眠质量']
        values = [
            self.user_data['weight'] / (self.user_data['height']/100)**2,
            min(self.user_data['steps']/10000*100, 120),
            min(self.user_data['sleep']/8*100, 120)
        ]
        
        bars = ax.bar(metrics, values, color=['#2ecc71', '#3498db', '#9b59b6'])
        ax.set_facecolor('#f8f9fa')
        ax.set_ylim(0, 120)
        ax.set_ylabel('健康指数 (%)', fontproperties=get_font_prop(fm))
        ax.set_title('您的健康数据概览', fontproperties=get_font_prop(fm), pad=20)
        
        # 设置字体
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(get_font_prop(fm))
        
        # 添加数据标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom',
                    fontproperties=get_font_prop(fm))
        
        plt.tight_layout()
        
        # 嵌入图表
        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        """分析与建议标签页"""
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text='📝 分析与建议')
        
        # 报告内容
        report_text = (
            f"【综合健康报告】\n\n"
            f"• BMI指数：{report['bmi']['value']} ({report['bmi']['category']})\n"
            f"• 运动建议：{report['exercise']}\n"
            f"• 睡眠评估：{report['mental_health']}\n"
            f"• 天气提示：{report['weather_impact']}\n\n"
        )
        
        text_area = tk.Text(text_frame, wrap=tk.WORD, font=('Microsoft YaHei', 11),
                        padx=15, pady=15, bg='#f8f9fa', relief='flat')
        text_area.insert(tk.END, report_text)
        text_area.config(state=tk.DISABLED)
        text_area.pack(fill='both', expand=True)
        
        # 底部状态栏
        status_bar = ttk.Frame(report_window)
        status_bar.pack(fill='x', padx=5, pady=5)
        ttk.Label(status_bar, 
                text=f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                relief='sunken').pack(side='left')
        ttk.Button(status_bar, text="完成", 
                command=lambda: report_window.destroy()).pack(side='right')

if __name__ == "__main__":
    root_path = resource_path("")
    os.chdir(root_path)
    print(f"sys: change work path to {root_path} successfully.")

    root = tk.Tk()
    app = HealthGuardian(root)
    root.mainloop()