import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect('d:/codeedu/codeedu.db')
cursor = conn.cursor()

print("检查数据库中的用户和密码哈希:")
print("=" * 60)

# 获取所有用户
cursor.execute('SELECT username, password_hash FROM users')
users = cursor.fetchall()

for user in users:
    username = user[0]
    db_hash = user[1]
    test_hash = hash_password('123456')
    matches = db_hash == test_hash
    
    print(f"用户: {username}")
    print(f"  数据库哈希: {db_hash}")
    print(f"  123456哈希: {test_hash}")
    print(f"  匹配: {'是' if matches else '否'}")
    print()

conn.close()

print("=" * 60)
print("测试simple_server.py中的哈希函数:")
print(f"  hash_password('123456'): {hash_password('123456')}")
