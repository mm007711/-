#!/bin/bash

echo "========================================"
echo "   CodeEdu 在线编程教学平台 - 完整便携版"
echo "========================================"
echo ""
echo "[版本] 2.0.0 (完整版)"
echo "[打包] 2025-03-27"
echo "[用途] 教学演示与评估"
echo "[支持] 计算机学院"
echo ""
echo "[启动] 正在启动系统..."
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3"
    echo ""
    echo "[提示] 解决方案:"
    echo "   1. 访问 https://www.python.org/downloads/"
    echo "   2. 下载并安装Python 3.8+"
    echo ""
    exit 1
fi

echo "[服务] 启动后端服务器..."
python3 backend/simple_server.py &
SERVER_PID=$!

echo "[等待] 等待服务器启动..."
sleep 3

echo "[前端] 打开教学平台..."
if command -v xdg-open &> /dev/null; then
    xdg-open "111.html"
elif command -v open &> /dev/null; then
    open "111.html"
else
    echo "请在浏览器中打开: 111.html"
fi

echo ""
echo "[成功] 系统启动成功！"
echo ""
echo "[功能] 完整功能列表:"
echo "   - 多班级管理系统 ✓"
echo "   - 可视化统计图表 ✓"
echo "   - 批量操作功能 ✓"
echo "   - 专业报告生成 ✓"
echo "   - 比赛/测验管理 ✓"
echo "   - 在线编程判题 ✓"
echo "   - 数据导入导出 ✓"
echo "   - 演示模式支持 ✓"
echo "   - 系统测试工具 ✓"
echo "   - 数据库检查 ✓"
echo "   - 用户管理 ✓"
echo ""
echo "[数据] 演示数据:"
echo "   - 2个班级，20名学生"
echo "   - 2场比赛，3道题目"
echo "   - 完整成绩和活跃度数据"
echo ""
echo "[工具] 可用工具:"
echo "   - import_demo_data.py (数据导入)"
echo "   - data_import_tool.py (批量导入)"
echo "   - add_more_problems.py (题目添加)"
echo "   - check_db.py (数据库检查)"
echo "   - test_system.py (系统测试)"
echo ""
echo "[注意] 按 Ctrl+C 停止服务器"
echo ""
echo "[演示] 现在可以开始给领导演示了！"
echo ""

# 等待用户中断
wait $SERVER_PID
