# GitHub推送指南

## 步骤1：在GitHub上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `codeedu`
   - Description: `在线编程评测系统 - 支持教学、竞赛和练习`
   - 选择 Public（公开）或 Private（私有）
   - 不要初始化README、.gitignore或license（因为本地已有）

3. 点击 "Create repository"

## 步骤2：添加远程仓库并推送

### 方法A：使用HTTPS（推荐初学者）
```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/codeedu.git

# 验证远程仓库
git remote -v

# 推送代码到GitHub
git push -u origin master
```

### 方法B：使用SSH（需要配置SSH密钥）
```bash
# 添加远程仓库
git remote add origin git@github.com:YOUR_USERNAME/codeedu.git

# 验证远程仓库
git remote -v

# 推送代码到GitHub
git push -u origin master
```

## 步骤3：处理可能的推送错误

### 如果遇到 "remote origin already exists" 错误：
```bash
# 先移除现有的远程仓库
git remote remove origin

# 然后重新添加
git remote add origin https://github.com/YOUR_USERNAME/codeedu.git
```

### 如果遇到 "failed to push some refs" 错误：
```bash
# 先拉取远程更改（如果有）
git pull origin master --allow-unrelated-histories

# 然后推送
git push -u origin master
```

## 步骤4：验证推送成功

1. 访问你的GitHub仓库：`https://github.com/YOUR_USERNAME/codeedu`
2. 确认以下文件已成功上传：
   - `README.md` - 项目文档
   - `backend/` - 后端代码
   - `frontend/` - 前端代码
   - `codeedu.db` - 数据库文件
   - 各种工具脚本和文档

## 步骤5：设置仓库信息（可选）

### 添加仓库标签
```bash
# 添加标签
git tag -a v1.0.0 -m "初始版本：完整核心功能"

# 推送标签
git push origin --tags
```

### 添加.gitignore（如果需要）
项目已包含`.gitignore`文件，但可以检查是否需要添加更多忽略规则。

## 步骤6：后续开发工作流

### 日常开发流程
```bash
# 1. 拉取最新代码
git pull origin master

# 2. 创建新分支
git checkout -b feature/new-feature

# 3. 开发并提交
git add .
git commit -m "feat: 添加新功能"

# 4. 推送到远程分支
git push origin feature/new-feature

# 5. 在GitHub创建Pull Request
```

### 版本发布流程
```bash
# 1. 更新版本号
# 2. 更新CHANGELOG.md
# 3. 提交版本更新
git add .
git commit -m "chore: 发布v1.1.0"

# 4. 创建标签
git tag -a v1.1.0 -m "版本1.1.0：新增前端界面"

# 5. 推送代码和标签
git push origin master
git push origin --tags
```

## 重要文件说明

### 必须推送的文件
1. **代码文件**：所有Python、TypeScript、Vue文件
2. **配置文件**：package.json、requirements.txt等
3. **数据库文件**：codeedu.db（包含测试数据）
4. **文档文件**：README.md、各种指南文档

### 建议忽略的文件（已在.gitignore中）
1. **Python缓存文件**：`__pycache__/`、`*.pyc`
2. **Node.js模块**：`node_modules/`
3. **IDE配置文件**：`.vscode/`、`.idea/`
4. **环境变量文件**：`.env`、`.env.local`

## 仓库维护建议

### 1. 分支策略
- `master`：稳定版本，用于生产
- `develop`：开发分支，集成新功能
- `feature/*`：功能开发分支
- `hotfix/*`：紧急修复分支

### 2. 提交规范
- `feat:`：新功能
- `fix:`：bug修复
- `docs:`：文档更新
- `style:`：代码格式调整
- `refactor:`：代码重构
- `test:`：测试相关
- `chore:`：构建过程或辅助工具变动

### 3. 代码审查
- 所有更改通过Pull Request合并
- 至少需要1人审查通过
- 通过CI/CD流水线测试

## 问题排查

### 常见问题1：推送被拒绝
**原因**：权限不足或仓库不存在
**解决**：
1. 确认GitHub仓库URL正确
2. 确认有推送权限
3. 使用正确的认证方式（HTTPS密码或SSH密钥）

### 常见问题2：大文件推送失败
**原因**：GitHub有100MB文件大小限制
**解决**：
1. 检查是否有大文件：`git ls-files | xargs wc -l`
2. 使用Git LFS（Large File Storage）
3. 从仓库中移除大文件：`git filter-branch`

### 常见问题3：历史记录冲突
**原因**：本地和远程历史记录不一致
**解决**：
```bash
# 强制推送（谨慎使用，会覆盖远程历史）
git push -f origin master
```

## 下一步行动

1. **立即行动**：按照步骤2推送代码到GitHub
2. **配置CI/CD**：设置GitHub Actions自动化测试和部署
3. **邀请协作者**：邀请团队成员参与开发
4. **设置项目看板**：使用GitHub Projects管理任务
5. **启用GitHub Pages**：部署项目文档网站

## 获取帮助

- GitHub官方文档：https://docs.github.com
- Git教程：https://git-scm.com/doc
- 问题反馈：在仓库Issues中创建问题

---

**现在可以执行以下命令推送代码：**

```bash
# 替换YOUR_USERNAME为你的GitHub用户名
git remote add origin https://github.com/YOUR_USERNAME/codeedu.git
git push -u origin master
```

推送成功后，你的在线评测系统将正式在GitHub上开源！ 🎉
