import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 连接到数据库
conn = sqlite3.connect('d:/codeedu/codeedu.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 获取所有用户
cursor.execute('SELECT username, password_hash FROM users')
users = cursor.fetchall()

print("数据库中的用户:")
for user in users:
    print(f"  {user['username']}: {user['password_hash']}")

# 测试密码哈希
print("\n测试密码哈希:")
test_passwords = {
    'teacher': '123456',
    'student': '123456',
    'admin': 'admin123'
}

for username, password in test_passwords.items():
    hashed = hash_password(password)
    print(f"  {username}密码'123456'的哈希: {hashed}")
    
    # 检查数据库中是否有匹配的用户
    cursor.execute('SELECT username FROM users WHERE username = ? AND password_hash = ?', (username, hashed))
    match = cursor.fetchone()
    if match:
        print(f"    ✅ 匹配成功!")
    else:
        print(f"    ❌ 无匹配用户")

conn.close()
