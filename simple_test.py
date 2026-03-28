import urllib.request
import json

print("简单测试后端服务器...")

try:
    # 测试根路径
    req = urllib.request.Request('http://localhost:5000/')
    response = urllib.request.urlopen(req)
    print("服务器根路径响应正常")
except Exception as e:
    print(f"服务器根路径错误: {e}")

try:
    # 测试登录API（不带数据，看是否返回405）
    req = urllib.request.Request('http://localhost:5000/api/auth/login', method='GET')
    response = urllib.request.urlopen(req)
    print("登录API响应正常")
except Exception as e:
    print(f"登录API错误（预期）: {e}")
