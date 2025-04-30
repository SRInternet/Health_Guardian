<div align="left">

# <image src="https://github.com/user-attachments/assets/e7b2dca0-7545-4f54-a076-9248b2498f35" height="40"/>   Health Guardian
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FSRInternet%2FHealth_Guardian.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FSRInternet%2FHealth_Guardian?ref=badge_small)
 <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
 <img src="https://img.shields.io/badge/language-python-blue" alt="Language">
 <img src="https://img.shields.io/badge/FREE-100%25-brightgreen" alt="FREE">

一个融合多学科领域的智能健康计算软件，通过多维度数据分析提供个性化健康建议。<br/>

</div>

---

## 🧠 设计理念

### 1. 多学科领域融合架构
| 学科领域       | 实现功能                          | 技术方案                  |
|----------------|-----------------------------------|---------------------------|
| **生物医学**   | BMI计算/睡眠质量评估               | 根据医学推荐标准计算         |
| **环境科学**   | 实时天气影响分析                   | 腾讯天气API集成             |
| **体育科学**   | 运动建议                          | 根据医学推荐标准计算         |

### 2. 模块化设计
```
核心系统架构：
├── 数据采集层（前端用户交互）
│   ├── 用户健康信息
│   └── 环境地理位置
├── 分析引擎层（后端数据计算）
│   ├── 健康分析模块
│   ├── 天气分析模块
│   └── ......
└── 输出层（展示对话框）
    ├── 可视化图标生成系统
    └── 生活建议生成系统
```

---

## 💡 创新亮点

### 技术突破
- **智能数据融合**
  - 实现生理数据与环境数据的动态关联分析

- **跨平台可视化**
  - 支持 Matplotlib 图表 + Tkinter UI混合渲染
  - 自适应字体适配技术

### 学科交叉
- **生物医学与环境科学**
  - 降雨出行安全建议

- **生物医学与体育科学**
  - 运动数据分析与运动建议

---

## 🚀 快速开始

### 安装要求
```bash
# 依赖安装
pip install requests matplotlib

# 字体配置
cp assets/Text.ttf ~/.fonts/  # Linux/macOS neccessary
```

### 使用指南
1. **数据输入界面**
   
   ![UI示意图](https://github.com/user-attachments/assets/140e3f81-bd81-4b27-9926-6769bd1cccf7)
   - 必填字段验证
   - 字段有效性验证

2. **健康分析流程**
   ```mermaid
   graph TD
   A[输入个人信息和位置信息] --> B[点击【健康分析】] --> C{后端计算+天气API调用}
   C -->|成功| D[展示信息窗口]
   C -->|失败| E[错误提示定位]
   ```
   
---

## 🔧 二次开发指南

### MIT协议规范

允许：
- 商业使用
- 修改发行
- 私有部署

要求：
- 保留版权声明
- 包含许可文件

禁止：
- 作者责任追究

### 扩展开发建议
1. **数据源扩展**
   ```python
   class ExtendedHealthData(HealthGuardian):
       def add_air_quality(self):
           # 接入空气质量API
           pass
   ```

2. **分析模型优化**
   ```python
   # 在generate_report()中添加
   def new_genetic_analysis(self):
       """新增基因数据分析"""
       return DNAAnalyzer.run(self.user_data)
   ```

3. **硬件集成方案**
   ```python
   # 示例蓝牙手环数据对接
   import bluetooth
   def sync_bracelet_data(self):
       return bluetooth.receive_fitness_data()
   ```

---

**贡献指南**: 欢迎提交PR！请遵循PEP8规范并附带单元测试
