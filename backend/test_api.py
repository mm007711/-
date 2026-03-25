#!/usr/bin/env python3
"""
测试API脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    """测试认证"""
    print("=== 测试认证 ===")
    
    # 测试登录
    data = {
        "username": "test_student",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✓ 登录成功，token: {token[:20]}...")
            
            # 测试获取用户信息
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"✓ 获取用户信息成功: {user['username']} ({user['role']})")
                return token
            else:
                print(f"✗ 获取用户信息失败: {response.status_code}")
        else:
            print(f"✗ 登录失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    
    return None

def test_problems(token):
    """测试题目API"""
    print("\n=== 测试题目API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 获取题目列表
        response = requests.get(f"{BASE_URL}/api/problems", headers=headers)
        if response.status_code == 200:
            problems = response.json()
            print(f"✓ 获取题目列表成功: {len(problems)} 个题目")
            for problem in problems[:2]:  # 显示前2个
                print(f"  - {problem['title']} ({problem['difficulty']})")
        else:
            print(f"✗ 获取题目列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

def test_contests(token):
    """测试比赛API"""
    print("\n=== 测试比赛API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 获取比赛列表
        response = requests.get(f"{BASE_URL}/api/contests", headers=headers)
        if response.status_code == 200:
            contests = response.json()
            print(f"✓ 获取比赛列表成功: {len(contests)} 个比赛")
            for contest in contests:
                print(f"  - {contest['title']}")
        else:
            print(f"✗ 获取比赛列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

def test_classes(token):
    """测试班级API"""
    print("\n=== 测试班级API ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 获取班级列表
        response = requests.get(f"{BASE_URL}/api/classes", headers=headers)
        if response.status_code == 200:
            classes = response.json()
            print(f"✓ 获取班级列表成功: {len(classes)} 个班级")
            for class_ in classes:
                print(f"  - {class_['name']}")
        else:
            print(f"✗ 获取班级列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

def test_judge(token):
    """测试评测API"""
    print("\n=== 测试评测API ===")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 简单的Python代码
    code = """
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# 测试代码
import sys
import json

if __name__ == "__main__":
    data = sys.stdin.read().strip().split('\\n')
    if len(data) >= 2:
        nums = json.loads(data[0])
        target = int(data[1])
        result = two_sum(nums, target)
        print(json.dumps(result))
"""
    
    try:
        # 使用旧API进行评测
        response = requests.post(
            f"{BASE_URL}/api/judge/run?problem_id=4",  # Two Sum的ID
            headers=headers,
            json={"code": code}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 评测成功: {result['status']}")
            print(f"  报告: {result['report']}")
            print(f"  分数: {result['score']}")
            print(f"  通过用例: {result['passed_cases']}/{result['total_cases']}")
        else:
            print(f"✗ 评测失败: {response.status_code}")
            print(f"  响应: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

def main():
    print("开始测试API...")
    
    # 等待服务器启动
    import time
    time.sleep(2)
    
    token = test_auth()
    if token:
        test_problems(token)
        test_contests(token)
        test_classes(token)
        test_judge(token)
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
