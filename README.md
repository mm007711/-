# CodeEdu - 在线编程教学平台

> 一个完整的在线编程教学与练习系统，采用Vue 3 + TypeScript前端 + FastAPI后端架构

## 📁 目录结构

```
codeedu/
├─ prototype/          # 原始原型（参考用，不再维护）
│  └─ index.html
├─ frontend/           # Vue 3 前端工程
├─ backend/            # FastAPI 后端工程
├─ docs/               # 接口文档、数据库设计、原型说明
├─ .gitignore
└─ README.md           # 本文件
```

## 🎯 功能模块

### 核心功能
- **题库管理**：公共题库、题目导入导出
- **在线编码**：多语言代码编辑器（Python、JavaScript等）
- **判题系统**：实时反馈、测试用例管理
- **比赛/测验**：组卷、在线考试、成绩统计
- **班级管理**：学生名单、成绩单导出
- **提交记录**：历史追踪、详细分析

### 技术亮点
- 浏览器沙箱隔离执行
- 本地数据持久化
- 多角色权限管理（学生/教师/管理员）
- 响应式设计

## 🚀 快速开始

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`

### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 `http://localhost:8000/docs`

## 📝 开发计划

- [x] 原型设计与验证
- [ ] 前端Vue 3框架搭建
- [ ] 后端FastAPI服务搭建
- [ ] 数据库设计与迁移
- [ ] API端点实现
- [ ] 性能优化与测试
- [ ] 部署与上线

## 📖 文档

详见 `docs/` 目录：
- API接口文档
- 数据库Schema设计
- 原型功能说明
- 部署指南

## 📄 License

MIT
