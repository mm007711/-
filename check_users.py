#!/usr/bin/env python3
"""
检查用户数据
"""

import sqlite3
import hashlib

def check_users():
    print("检查用户数据...")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    # 获取所有用户
    cursor.execute("SELECT id, username, password_hash, name, role FROM users")
    users = cursor.fetchall()
    
    print(f"用户列表 ({len(users)} 个用户):")
    for user in users:
        user_id, username, password_hash, name, role = user
        print(f"\nID: {user_id}")
        print(f"  用户名: {username}")
        print(f"  密码哈希: {password_hash}")
        print(f"  姓名: {name}")
        print(f"  角色: {role}")
        
        # 测试密码 'test123' 的哈希
        test_hash = hashlib.sha256('test123'.encode()).hexdigest()
        print(f"  'test123' 的哈希: {test_hash}")
        print(f"  哈希匹配: {'是' if password_hash == test_hash else '否'}")
    
    conn.close()

if __name__ == "__main__":
    check_users()
