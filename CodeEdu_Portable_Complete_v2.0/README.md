# CodeEdu 在线编程教学平台 - 完整便携版 v2.0

## 平台简介

CodeEdu 是一个功能完整的在线编程教学平台，专为计算机教育设计。此完整版包含了所有用户添加的功能和工具，平台集成了多班级管理、可视化数据分析、批量操作、专业报告生成等核心功能，适合教学演示、课堂使用和领导评估。

## 🚀 快速开始

### Windows 用户
1. 双击运行 `启动教学平台.bat`
2. 系统会自动启动后端服务器
3. 浏览器会自动打开教学平台界面

### Linux/Mac 用户
1. 打开终端
2. 运行命令: `./启动教学平台.sh`
3. 系统会自动启动后端服务器
4. 浏览器会自动打开教学平台界面

## 🎯 完整功能列表

### 1. 多班级管理系统 [完整版]
- **创建/编辑/删除**多个班级
- **一键切换**不同班级
- **学生数据**独立存储
- **班级统计**实时更新
- **批量操作**支持

### 2. 可视化统计图表 [完整版]
- **成绩分布**柱状图
- **活跃度趋势**折线图
- **实时刷新**功能
- **响应式**设计
- **图表导出**支持

### 3. 批量操作功能 [完整版]
- **批量选择**学生
- **批量移除**操作
- **分页浏览**支持
- **状态提示**显示
- **数据校验**功能

### 4. 专业报告生成 [完整版]
- **一键生成**班级分析报告
- **打印支持**功能
- **专业格式**输出
- **数据导出**CSV/JSON
- **报告模板**定制

### 5. 比赛/测验管理 [完整版]
- **创建编程**比赛
- **题目组卷**功能
- **比赛状态**管理
- **参与统计**显示
- **成绩分析**功能

### 6. 在线编程判题 [完整版]
- **支持Python/JavaScript**
- **实时代码**执行
- **自动判题**评分
- **测试用例**管理
- **代码高亮**显示

### 7. 数据管理工具 [新增]
- **批量数据导入** (data_import_tool.py)
- **演示数据导入** (import_demo_data.py)
- **题目批量添加** (add_more_problems.py)
- **数据库检查** (check_db.py)
- **用户检查** (check_users.py)

### 8. 系统测试工具 [新增]
- **系统功能测试** (test_system.py)
- **演示环境检查** (check_demo_env.py)
- **API接口测试** (backend/test_api.py)
- **性能测试**支持

### 9. 演示模式支持 [新增]
- **一键演示**功能
- **自动流程**展示
- **演示脚本**支持
- **演示页面** (demo.html)

## 📋 演示指南

### 第一步: 导入演示数据
1. 打开平台后，切换到"**教师/管理员**"视角
2. 点击"**导入/发布题目JSON**"按钮
3. 选择 `demo_class_data.json` 文件
4. 点击"**保存并导入**"

### 第二步: 体验核心功能
1. **班级管理演示**: 创建新班级，切换不同班级
2. **批量操作演示**: 勾选学生，尝试批量移除
3. **可视化演示**: 查看成绩分布和活跃度趋势
4. **报告生成演示**: 点击"生成报告"查看专业分析
5. **比赛管理演示**: 查看现有比赛，尝试创建新比赛

### 第三步: 使用工具演示
1. **数据导入工具**: 运行 `python data_import_tool.py`
2. **系统测试工具**: 运行 `python test_system.py`
3. **数据库检查**: 运行 `python check_db.py`
4. **演示环境检查**: 运行 `python check_demo_env.py`

## 🛠️ 可用工具说明

### 1. data_import_tool.py
- 功能: 批量导入学生、题目、比赛数据
- 用法: `python data_import_tool.py --help`
- 支持格式: JSON, CSV

### 2. import_demo_data.py
- 功能: 导入演示数据到系统
- 用法: `python import_demo_data.py`
- 数据文件: demo_class_data.json

### 3. add_more_problems.py
- 功能: 批量添加编程题目
- 用法: `python add_more_problems.py`
- 支持: 自定义题目模板

### 4. check_db.py
- 功能: 检查数据库状态和数据完整性
- 用法: `python check_db.py`
- 输出: 数据库状态报告

### 5. check_demo_env.py
- 功能: 检查演示环境是否正常
- 用法: `python check_demo_env.py`
- 检查项: Python版本、依赖包、文件完整性

### 6. check_users.py
- 功能: 检查用户数据完整性
- 用法: `python check_users.py`
- 检查项: 用户数量、数据格式、关联关系

### 7. test_system.py
- 功能: 系统功能测试
- 用法: `python test_system.py`
- 测试项: API接口、数据库操作、判题功能

## 📁 文件结构

```
CodeEdu_Portable_Complete_v2.0/
├── 启动教学平台.bat              # Windows启动脚本
├── 启动教学平台.sh               # Linux/Mac启动脚本
├── 111.html                     # 主应用文件
├── demo.html                    # 演示页面
├── demo_class_data.json         # 演示数据
├── codeedu_export.json          # 导出数据示例
├── config.json                  # 配置文件
├── import_demo_data.py          # 数据导入脚本
├── data_import_tool.py          # 批量数据导入工具
├── add_more_problems.py         # 题目批量添加工具
├── check_db.py                  # 数据库检查工具
├── check_demo_env.py            # 演示环境检查工具
├── check_users.py               # 用户检查工具
├── test_system.py               # 系统测试工具
├── demo-mode-simple.js          # 演示模式脚本
├── demo-mode.js                 # 高级演示脚本
├── sample_users.csv             # 用户数据示例
├── README.md                    # 本说明文档
├── DEMO_GUIDE.md                # 演示指南
├── DEMO_PREPARATION_SUMMARY.md  # 演示准备总结
├── CLASS_MANAGEMENT_OPTIMIZATION_SUMMARY.md  # 班级管理优化总结
├── FUNCTIONALITY_VERIFICATION_REPORT.md      # 功能验证报告
├── GITHUB_PUSH_GUIDE.md         # GitHub推送指南
├── INTEGRATION_PLAN.md          # 集成计划
├── INTEGRATION_SUMMARY.md       # 集成总结
├── LOGIC_FIXES_SUMMARY.md       # 逻辑修复总结
├── production_readiness.md      # 生产就绪报告
├── PROJECT_ROADMAP.md           # 项目路线图
├── system_summary.md            # 系统总结
└── backend/                     # 后端代码
    ├── simple_server.py         # 简易服务器
    ├── main.py                  # 主后端文件
    ├── models.py                # 数据模型
    ├── database.py              # 数据库操作
    ├── judge.py                 # 判题引擎
    ├── schemas.py               # 数据模式
    ├── init_test_data_simple.py # 测试数据
    ├── init_test_data.py        # 完整测试数据
    └── test_api.py              # API测试
```

## 给领导演示的重点

### 1. 专业性展示
- **多班级管理**体现系统完整性
- **可视化图表**展示数据分析能力
- **专业报告**体现系统成熟度
- **完整工具链**展示工程能力

### 2. 实用性展示
- **批量操作**提高工作效率
- **数据导出**方便数据管理
- **比赛管理**支持教学活动
- **测试工具**保证系统质量

### 3. 技术性展示
- **在线判题**体现技术实力
- **响应式设计**展示前端能力
- **模块化架构**体现工程水平
- **完整文档**展示专业态度

### 4. 扩展性展示
- **JSON导入**支持数据扩展
- **多语言支持**体现国际化
- **配置灵活**展示可定制性
- **工具齐全**支持二次开发

## 常见问题

### Q: 启动时提示"未检测到Python"？
A: 请安装Python 3.8+，安装时勾选"Add Python to PATH"

### Q: 导入数据后不显示？
A: 刷新页面或重新打开111.html

### Q: 如何重置所有数据？
A: 清除浏览器缓存或使用隐私模式

### Q: 支持多少学生数据？
A: 理论上无限制，建议单班级不超过1000人

### Q: 数据安全吗？
A: 数据存储在浏览器LocalStorage中，本地运行无网络传输

### Q: 如何添加更多题目？
A: 使用add_more_problems.py工具批量添加

### Q: 如何检查系统状态？
A: 使用test_system.py进行系统测试

## 技术支持

- **开发部门**: 计算机学院
- **用途**: 教学演示与评估
- **版本**: v2.0.0 (完整版)
- **打包时间**: 2025-03-27
- **文件数量**: 约40个文件
- **总大小**: 约0.5MB

## 开始演示

现在您可以:
1. 双击启动脚本开始系统
2. 按照演示指南操作
3. 向领导展示完整功能
4. 使用工具演示专业能力
5. 导出数据证明实用性

**祝您演示成功！**
