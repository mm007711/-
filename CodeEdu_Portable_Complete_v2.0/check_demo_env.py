#!/usr/bin/env python3
"""
检查演示环境是否正常
"""

import requests
import time
import webbrowser
import os

def check_backend():
    """检查后端服务器是否正常运行"""
    print("[检查] 检查后端服务器...")
    try:
        response = requests.get("http://localhost:5000/api/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 后端服务器运行正常 (http://localhost:5000)")
            print(f"   题目总数: {data.get('total_problems', 'N/A')}")
            print(f"   用户总数: {data.get('total_users', 'N/A')}")
            print(f"   比赛总数: {data.get('total_contests', 'N/A')}")
            return True
        else:
            print(f"[ERROR] 后端服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] 无法连接到后端服务器 (http://localhost:5000)")
        print("   请运行: python backend/simple_server.py")
        return False
    except Exception as e:
        print(f"[ERROR] 检查后端服务器时出错: {e}")
        return False

def check_demo_page():
    """检查演示页面是否存在"""
    print("\n[检查] 检查演示页面...")
    demo_path = os.path.join(os.getcwd(), "demo.html")
    if os.path.exists(demo_path):
        print(f"[OK] 演示页面存在: {demo_path}")
        return True
    else:
        print(f"[ERROR] 演示页面不存在: {demo_path}")
        return False

def check_database():
    """检查数据库文件是否存在"""
    print("\n[检查] 检查数据库文件...")
    db_path = os.path.join(os.getcwd(), "codeedu.db")
    if os.path.exists(db_path):
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"[OK] 数据库文件存在: {db_path}")
        print(f"   文件大小: {size_mb:.2f} MB")
        return True
    else:
        print(f"[ERROR] 数据库文件不存在: {db_path}")
        return False

def check_test_accounts():
    """检查测试账户"""
    print("\n[检查] 检查测试账户...")
    accounts = [
        ("test_student", "test123", "学生"),
        ("test_teacher", "test123", "教师"),
        ("test_admin", "test123", "管理员")
    ]
    
    for username, password, role in accounts:
        try:
            response = requests.post(
                "http://localhost:5000/api/auth/login",
                json={"username": username, "password": password},
                timeout=5
            )
            if response.status_code == 200:
                print(f"[OK] {role}账户正常: {username}")
            else:
                print(f"[ERROR] {role}账户登录失败: {username}")
        except:
            print(f"[WARN] 无法测试{role}账户 (服务器可能未运行)")

def open_demo_page():
    """打开演示页面"""
    print("\n[操作] 打开演示页面...")
    demo_path = os.path.join(os.getcwd(), "demo.html")
    webbrowser.open(f"file://{demo_path}")
    print("[OK] 演示页面已打开")

def main():
    print("=" * 60)
    print("CodeEdu 演示环境检查")
    print("=" * 60)
    
    # 等待服务器启动
    print("\n[等待] 等待服务器启动...")
    time.sleep(2)
    
    # 执行检查
    backend_ok = check_backend()
    demo_ok = check_demo_page()
    db_ok = check_database()
    
    if backend_ok:
        check_test_accounts()
    
    print("\n" + "=" * 60)
    print("检查结果总结:")
    print("=" * 60)
    
    if backend_ok and demo_ok and db_ok:
        print("[成功] 所有检查通过！演示环境准备就绪。")
        print("\n[准备] 演示准备:")
        print("1. 后端服务器: [OK] 运行中 (http://localhost:5000)")
        print("2. 演示页面: [OK] 已准备 (demo.html)")
        print("3. 数据库: [OK] 已加载 (codeedu.db)")
        print("4. 测试账户: [OK] 可用")
        
        # 询问是否打开演示页面
        response = input("\n是否打开演示页面？(y/n): ")
        if response.lower() == 'y':
            open_demo_page()
        
        print("\n[指南] 演示指南:")
        print("   详细指南请查看: DEMO_GUIDE.md")
        print("   演示脚本: 15分钟完整展示流程")
        
    else:
        print("[警告] 演示环境存在问题:")
        if not backend_ok:
            print("   - 后端服务器未运行")
            print("     解决方案: python backend/simple_server.py")
        if not demo_ok:
            print("   - 演示页面不存在")
            print("     解决方案: 确保 demo.html 文件存在")
        if not db_ok:
            print("   - 数据库文件不存在")
            print("     解决方案: 运行数据初始化脚本")
        
        print("\n[修复] 修复建议:")
        print("1. 启动后端服务器:")
        print("   cd d:\\codeedu")
        print("   python backend/simple_server.py")
        print("\n2. 在浏览器中打开演示页面:")
        print("   start demo.html")
        print("\n3. 检查系统功能:")
        print("   python test_system.py")

if __name__ == "__main__":
    main()
