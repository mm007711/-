# CodeEdu Netlify 部署指南

## 概述

本文档提供将CodeEdu教学平台部署到Netlify的完整指南。Netlify是一个现代化的静态网站托管平台，支持自动部署、CDN加速和HTTPS。

## 部署选项

### 选项1：GitHub自动部署（推荐）

#### 步骤1：准备GitHub仓库
```bash
# 1. 初始化Git仓库
git init
git add .
git commit -m "初始提交：CodeEdu教学平台v2.0"

# 2. 创建GitHub仓库
# 访问 https://github.com/new
# 创建名为 codeedu 的仓库

# 3. 关联远程仓库并推送
git remote add origin https://github.com/你的用户名/codeedu.git
git branch -M main
git push -u origin main
```

#### 步骤2：Netlify部署
1. 访问 https://app.netlify.com
2. 使用GitHub账号登录
3. 点击 "New site from Git"
4. 选择GitHub作为Git提供商
5. 授权Netlify访问GitHub仓库
6. 选择 `codeedu` 仓库
7. 配置部署设置：
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/dist`
8. 点击 "Deploy site"

#### 步骤3：自定义域名（可选）
1. 在Netlify控制台选择你的站点
2. 进入 "Domain settings"
3. 点击 "Add custom domain"
4. 输入你的域名并按照指引配置DNS

### 选项2：Netlify CLI手动部署

#### 安装Netlify CLI
```bash
# 全局安装Netlify CLI
npm install -g netlify-cli
```

#### 登录Netlify
```bash
# 浏览器登录
netlify login
```

#### 初始化项目
```bash
# 进入项目目录
cd d:\codeedu

# 初始化Netlify项目
netlify init
```

#### 部署到Netlify
```bash
# 部署到草稿环境
netlify deploy

# 部署到生产环境
netlify deploy --prod
```

### 选项3：直接拖放部署

1. 构建前端项目：
```bash
cd frontend
npm install
npm run build
```

2. 访问 https://app.netlify.com
3. 将 `frontend/dist` 文件夹拖放到Netlify的部署区域

## 项目配置

### Netlify配置文件 (netlify.toml)
```toml
[build]
  command = "cd frontend && npm run build"
  publish = "frontend/dist"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[dev]
  command = "cd frontend && npm run dev"
  port = 5173
  publish = "frontend/dist"
```

### 环境变量配置

如果需要配置环境变量，在Netlify控制台：
1. 进入站点设置
2. 选择 "Environment variables"
3. 添加以下变量（如果需要）：
   - `VITE_API_URL`: 后端API地址
   - `VITE_APP_TITLE`: 应用标题

## 静态演示版本

我们还创建了一个专门的静态演示版本，位于 `static-demo/` 目录：

### 部署静态演示
```bash
# 方法1：直接部署static-demo目录
# 将static-demo目录拖放到Netlify

# 方法2：修改netlify.toml配置
# 修改publish目录为 "static-demo"
```

### 静态演示功能
- ✅ 多角色登录演示
- ✅ 在线编程演示
- ✅ 核心功能展示
- ✅ 部署指南
- ✅ 响应式设计
- ✅ 无需后端API

## 后端API部署说明

### 重要提示
完整的CodeEdu平台需要后端API支持。Netlify主要托管静态前端，后端需要单独部署：

### 后端部署选项
1. **Vercel**：支持Python Flask应用
2. **Railway**：全栈应用部署平台
3. **Heroku**：传统PaaS平台
4. **国内云服务**：阿里云、腾讯云等

### 前后端分离配置
如果后端部署在其他平台，需要配置前端API地址：

```bash
# 创建前端环境配置文件
# frontend/.env.production
VITE_API_URL=https://your-backend-api.com
```

## 部署验证

### 检查清单
- [ ] 前端构建成功
- [ ] Netlify部署完成
- [ ] 网站可正常访问
- [ ] HTTPS自动启用
- [ ] 自定义域名配置（如需要）
- [ ] 环境变量配置正确

### 测试步骤
1. 访问Netlify提供的域名（如：`https://your-site.netlify.app`）
2. 测试所有演示功能
3. 检查控制台是否有错误
4. 测试响应式布局

## 常见问题

### Q1: 构建失败
**问题**：`npm run build` 失败
**解决**：
1. 检查Node.js版本（需要Node.js 16+）
2. 清理npm缓存：`npm cache clean --force`
3. 重新安装依赖：`rm -rf node_modules && npm install`

### Q2: 页面空白
**问题**：部署后页面空白
**解决**：
1. 检查控制台错误
2. 确认路由配置正确
3. 检查 `_redirects` 文件配置

### Q3: API请求失败
**问题**：前端无法连接后端API
**解决**：
1. 配置正确的API地址
2. 检查CORS配置
3. 确保后端服务正常运行

### Q4: 静态资源404
**问题**：CSS/JS文件加载失败
**解决**：
1. 检查构建输出路径
2. 确认资源引用路径正确
3. 检查Netlify的 `_headers` 配置

## 性能优化

### 构建优化
```bash
# 前端构建优化
cd frontend
npm run build -- --mode production
```

### Netlify功能
1. **CDN加速**：全球CDN网络
2. **自动HTTPS**：免费SSL证书
3. **图片优化**：自动图片压缩
4. **缓存策略**：智能缓存配置

### 监控和分析
1. **Netlify Analytics**：内置网站分析
2. **错误跟踪**：实时错误监控
3. **性能监控**：页面加载性能

## 更新和维护

### 自动部署
每次推送到GitHub主分支，Netlify会自动重新部署。

### 手动部署
```bash
# 更新代码后
git add .
git commit -m "更新描述"
git push origin main
```

### 回滚部署
在Netlify控制台可以轻松回滚到之前的部署版本。

## 联系支持

### 项目资源
- GitHub仓库：`https://github.com/你的用户名/codeedu`
- Netlify站点：`https://your-site.netlify.app`
- 在线文档：项目内文档文件

### 技术支持
- 问题反馈：GitHub Issues
- 文档更新：项目README
- 社区支持：技术论坛

## 总结

通过Netlify部署，CodeEdu教学平台可以获得：
- 🚀 快速全球访问
- 🔒 自动HTTPS安全
- 📱 响应式设计支持
- 🔄 自动持续部署
- 📊 内置分析监控
- 💰 免费基础套餐

现在您的CodeEdu教学平台已经准备好面向全球用户了！
