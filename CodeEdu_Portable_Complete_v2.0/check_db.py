#!/usr/bin/env python3
"""
检查数据库结构
"""

import sqlite3

def check_database():
    print("检查数据库结构...")
    
    try:
        conn = sqlite3.connect('codeedu.db')
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"数据库中有 {len(tables)} 个表:")
        for table in tables:
            table_name = table[0]
            print(f"\n表: {table_name}")
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("  列:")
            for col in columns:
                col_id, col_name, col_type, notnull, default_val, pk = col
                print(f"    {col_name} ({col_type})")
        
        conn.close()
        
        # 检查是否有必要的数据
        print("\n检查测试数据...")
        conn = sqlite3.connect('codeedu.db')
        cursor = conn.cursor()
        
        # 检查users表
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"  users表: {user_count} 条记录")
            
            if user_count == 0:
                print("  [WARNING] users表为空，需要创建测试用户")
        except sqlite3.OperationalError:
            print("  [ERROR] users表不存在")
        
        # 检查problems表
        try:
            cursor.execute("SELECT COUNT(*) FROM problems")
            problem_count = cursor.fetchone()[0]
            print(f"  problems表: {problem_count} 条记录")
        except sqlite3.OperationalError:
            print("  [ERROR] problems表不存在")
        
        # 检查contests表
        try:
            cursor.execute("SELECT COUNT(*) FROM contests")
            contest_count = cursor.fetchone()[0]
            print(f"  contests表: {contest_count} 条记录")
        except sqlite3.OperationalError:
            print("  [ERROR] contests表不存在")
        
        # 检查classes表
        try:
            cursor.execute("SELECT COUNT(*) FROM classes")
            class_count = cursor.fetchone()[0]
            print(f"  classes表: {class_count} 条记录")
        except sqlite3.OperationalError:
            print("  [ERROR] classes表不存在")
        
        conn.close()
        
    except Exception as e:
        print(f"检查数据库时出错: {e}")

if __name__ == "__main__":
    check_database()
