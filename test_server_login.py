import sys
sys.path.append('d:/codeedu/backend')

from simple_server import app, hash_password, get_db
import sqlite3

# 测试哈希函数
print("测试哈希函数:")
print(f"hash_password('123456'): {hash_password('123456')}")

# 直接测试数据库连接
print("\n测试数据库连接:")
conn = get_db()
cursor = conn.cursor()

cursor.execute('SELECT username, password_hash FROM users WHERE username = "test_teacher"')
user = cursor.fetchone()

if user:
    print(f"找到用户: {user['username']}")
    print(f"数据库哈希: {user['password_hash']}")
    print(f"123456哈希: {hash_password('123456')}")
    print(f"匹配: {user['password_hash'] == hash_password('123456')}")
    
    # 测试登录逻辑
    password = '123456'
    if user['password_hash'] == hash_password(password):
        print("✅ 密码验证成功!")
    else:
        print("❌ 密码验证失败!")
else:
    print("用户未找到")

conn.close()

# 测试其他用户
print("\n测试其他用户:")
conn = get_db()
cursor = conn.cursor()
cursor.execute('SELECT username, password_hash FROM users')
users = cursor.fetchall()

for u in users:
    matches = u['password_hash'] == hash_password('123456')
    print(f"{u['username']}: 匹配123456 = {matches}")

conn.close()
