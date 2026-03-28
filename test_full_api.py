import urllib.request
import json
import time

print("=" * 60)
print("CodeEdu 完整API测试")
print("=" * 60)

def test_api():
    try:
        # 1. 测试根路径
        print("\n1. 测试根路径...")
        req = urllib.request.Request('http://localhost:5000/')
        response = urllib.request.urlopen(req)
        root_data = json.load(response)
        print(f"   成功: {root_data['name']} v{root_data['version']}")
        
        # 2. 测试登录
        print("\n2. 测试登录API...")
        login_data = json.dumps({
            "username": "student1",
            "password": "123456"
        }).encode('utf-8')
        
        login_req = urllib.request.Request(
            'http://localhost:5000/api/auth/login',
            data=login_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        login_response = urllib.request.urlopen(login_req)
        login_result = json.load(login_response)
        token = login_result['access_token']
        print(f"   登录成功: {login_result['user']['username']} ({login_result['user']['role']})")
        
        # 3. 测试获取当前用户信息
        print("\n3. 测试获取当前用户信息...")
        me_req = urllib.request.Request(
            'http://localhost:5000/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        me_response = urllib.request.urlopen(me_req)
        me_result = json.load(me_response)
        print(f"   用户信息: {me_result['name']} ({me_result['email']})")
        
        # 4. 测试获取问题列表
        print("\n4. 测试获取问题列表...")
        problems_req = urllib.request.Request(
            'http://localhost:5000/api/problems',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        problems_response = urllib.request.urlopen(problems_req)
        problems_result = json.load(problems_response)
        print(f"   获取到 {len(problems_result)} 个问题")
        
        # 5. 测试获取比赛列表
        print("\n5. 测试获取比赛列表...")
        contests_req = urllib.request.Request(
            'http://localhost:5000/api/contests',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        contests_response = urllib.request.urlopen(contests_req)
        contests_result = json.load(contests_response)
        print(f"   获取到 {len(contests_result)} 个比赛")
        
        # 6. 测试获取班级列表
        print("\n6. 测试获取班级列表...")
        classes_req = urllib.request.Request(
            'http://localhost:5000/api/classes',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        classes_response = urllib.request.urlopen(classes_req)
        classes_result = json.load(classes_response)
        print(f"   获取到 {len(classes_result)} 个班级")
        
        # 7. 测试获取统计信息
        print("\n7. 测试获取统计信息...")
        stats_req = urllib.request.Request(
            'http://localhost:5000/api/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        stats_response = urllib.request.urlopen(stats_req)
        stats_result = json.load(stats_response)
        print(f"   系统统计: {stats_result['total_problems']}题, {stats_result['total_users']}用户")
        
        # 8. 测试创建新题目
        print("\n8. 测试创建新题目...")
        new_problem_data = json.dumps({
            "title": "测试题目 - 两数之和",
            "description": "给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那两个整数，并返回它们的数组下标。",
            "difficulty": "简单",
            "score": 10,
            "time_limit": 1000,
            "memory_limit": 256,
            "tags": "数组,哈希表",
            "is_public": True
        }).encode('utf-8')
        
        create_problem_req = urllib.request.Request(
            'http://localhost:5000/api/problems',
            data=new_problem_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        
        create_problem_response = urllib.request.urlopen(create_problem_req)
        create_problem_result = json.load(create_problem_response)
        print(f"   创建题目成功: {create_problem_result['title']} (ID: {create_problem_result['id']})")
        
        # 9. 测试评测功能
        print("\n9. 测试评测功能...")
        judge_data = json.dumps({
            "code": "def two_sum(nums, target):\n    hashmap = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hashmap:\n            return [hashmap[complement], i]\n        hashmap[num] = i\n    return []"
        }).encode('utf-8')
        
        judge_req = urllib.request.Request(
            'http://localhost:5000/api/judge/run?problem_id=1',
            data=judge_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        
        judge_response = urllib.request.urlopen(judge_req)
        judge_result = json.load(judge_response)
        print(f"   评测结果: {judge_result['status']}, 得分: {judge_result['score']}")
        
        print("\n" + "=" * 60)
        print("所有API测试通过！系统运行正常。")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\nAPI测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("等待服务器启动...")
    time.sleep(2)
    test_api()
