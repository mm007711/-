# CodeEdu - 在线编程评测系统

## 🎯 项目简介

CodeEdu 是一个功能完整的在线编程评测系统，支持编程教学、算法竞赛、班级管理和个人练习等多种场景。

## ✨ 核心功能

### 1. 用户系统
- 多角色权限：学生、教师、管理员
- JWT令牌认证
- 用户信息管理

### 2. 题目管理
- 题目CRUD操作
- 难度分类（简单、中等、困难）
- 题目标签系统
- 公开/私有题目控制

### 3. 评测系统
- 代码提交和自动评测
- 详细的判题结果
- 多种评测状态（AC、WA、TLE、MLE、RE等）
- 运行时间和内存统计

### 4. 比赛管理
- 比赛创建和时间控制
- 题目关联和分数设置
- 参赛者排名

### 5. 班级管理
- 班级创建和学生注册
- 成绩统计和进度跟踪
- 教师管理功能

### 6. 数据管理
- CSV数据导入（用户、题目、班级）
- JSON数据导出
- 批量操作支持

## 🏗️ 技术架构

### 后端技术栈
- **框架**：Flask (Python)
- **数据库**：SQLite
- **认证**：JWT令牌
- **API设计**：RESTful

### 前端技术栈
- **框架**：Vue.js 3 + TypeScript
- **状态管理**：Pinia
- **构建工具**：Vite
- **路由**：Vue Router

### 开发工具
- 数据导入工具 (`data_import_tool.py`)
- 系统测试脚本 (`test_system.py`)
- 数据库检查工具 (`check_db.py`, `check_users.py`)

## 🚀 快速开始

### 1. 环境准备
```bash
# 克隆项目
git clone https://github.com/yourusername/codeedu.git
cd codeedu

# 安装后端依赖
pip install flask flask-cors pyjwt

# 安装前端依赖
cd frontend
npm install
```

### 2. 启动后端服务器
```bash
cd backend
python simple_server.py
# 服务器运行在 http://localhost:5000
```

### 3. 启动前端开发服务器
```bash
cd frontend
npm run dev
# 前端运行在 http://localhost:5173
```

### 4. 测试系统
```bash
# 运行系统测试
python test_system.py
```

## 📊 系统数据

### 默认测试账户
1. **学生**：test_student / test123
2. **教师**：test_teacher / test123  
3. **管理员**：test_admin / test123

### 初始数据
- **用户**：8个（3个测试用户 + 5个示例用户）
- **题目**：16个（覆盖不同难度和主题）
- **比赛**：2个（示例比赛）
- **班级**：2个（示例班级）

## 🔧 数据管理

### 数据导入
```bash
# 导入用户
python data_import_tool.py import_users sample_users.csv

# 导入题目
python data_import_tool.py import_problems problems.csv

# 导入班级
python data_import_tool.py import_classes classes.csv
```

### 数据导出
```bash
# 导出所有数据
python data_import_tool.py export
# 生成 codeedu_export.json
```

## 📁 项目结构

```
codeedu/
├── backend/                    # 后端代码
│   ├── simple_server.py       # Flask服务器
│   ├── database.py           # 数据库连接
│   ├── models.py             # 数据模型
│   ├── schemas.py            # 数据模式
│   ├── judge.py              # 评测逻辑
│   └── test_api.py           # API测试
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── api/              # API接口
│   │   ├── components/       # Vue组件
│   │   ├── pages/           # 页面组件
│   │   ├── stores/          # 状态管理
│   │   └── router/          # 路由配置
│   └── package.json
├── docs/                      # 文档
├── tools/                     # 工具脚本
│   ├── data_import_tool.py   # 数据导入工具
│   ├── test_system.py        # 系统测试
│   ├── check_db.py           # 数据库检查
│   └── add_more_problems.py  # 题目添加工具
└── README.md                  # 项目说明
```

## 📈 生产就绪评估

### ✅ 已具备功能
- 完整的后端API
- 数据库结构和测试数据
- 数据导入导出工具
- 系统测试脚本
- 详细的文档

### ⚠️ 需要完善
- 前端界面开发
- 生产环境部署配置
- 性能优化和安全加固
- 更多编程语言支持

## 🎯 使用场景

### 1. 编程教学
- 教师创建班级，布置编程作业
- 学生提交代码，自动评测
- 成绩统计和进度跟踪

### 2. 算法竞赛
- 创建编程比赛
- 实时评测和排名
- 多种难度题目

### 3. 个人练习
- 丰富的算法题目库
- 详细的评测反馈
- 个人进度跟踪

### 4. 面试准备
- 常见面试题目
- 模拟真实评测环境
- 多种编程语言支持

## 🔮 未来发展

### 短期计划 (1-2个月)
- 完善前端用户界面
- 支持更多编程语言
- 增强评测系统

### 中期计划 (3-6个月)
- 社交功能（讨论区、排名）
- 智能推荐系统
- 移动端支持

### 长期计划 (6-12个月)
- 微服务架构重构
- 国际化支持
- 商业化功能

## 🤝 贡献指南

欢迎贡献代码、题目或文档！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目地址：https://github.com/yourusername/codeedu
- 问题反馈：https://github.com/yourusername/codeedu/issues

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**开始使用 CodeEdu，提升编程技能！** 🚀
