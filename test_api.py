import urllib.request
import json
import time

print("测试后端API连接...")
time.sleep(2)

try:
    # 测试登录API
    login_data = json.dumps({
        "username": "teacher",
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
    print(f"登录成功: {login_result['user']['username']}")
    
    # 使用token测试其他API
    token = login_result['access_token']
    
    # 测试获取问题列表
    problems_req = urllib.request.Request(
        'http://localhost:5000/api/problems',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    problems_response = urllib.request.urlopen(problems_req)
    problems_result = json.load(problems_response)
    print(f"获取到 {len(problems_result)} 个问题")
    
    # 测试获取统计信息
    stats_req = urllib.request.Request(
        'http://localhost:5000/api/stats',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    stats_response = urllib.request.urlopen(stats_req)
    stats_result = json.load(stats_response)
    print(f"系统统计: {stats_result}")
    
    print("\n✅ 所有API测试通过！")
    
except Exception as e:
    print(f"❌ API测试失败: {e}")
    import traceback
    traceback.print_exc()
