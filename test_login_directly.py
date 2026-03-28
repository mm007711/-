import sqlite3
import hashlib
import jwt
import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 连接到数据库
conn = sqlite3.connect('d:/codeedu/codeedu.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 测试test_teacher用户
username = 'test_teacher'
password = '123456'

cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
user = cursor.fetchone()

if user:
    print(f"找到用户: {user['username']}")
    print(f"数据库中的密码哈希: {user['password_hash']}")
    print(f"123456的哈希: {hash_password(password)}")
    print(f"哈希匹配: {user['password_hash'] == hash_password(password)}")
    
    if user['password_hash'] == hash_password(password):
        print("✅ 密码验证成功!")
        
        # 生成token
        SECRET_KEY = "your-secret-key-change-in-production"
        token = jwt.encode({
            'sub': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY)
        
        print(f"生成的Token: {token[:50]}...")
    else:
        print("❌ 密码验证失败!")
else:
    print(f"用户 {username} 未找到")

conn.close()
