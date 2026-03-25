#!/usr/bin/env python3
"""
数据导入工具 - 支持CSV/Excel文件导入
"""

import sqlite3
import csv
import json
import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def import_users_from_csv(csv_file):
    """从CSV文件导入用户"""
    print(f"从CSV文件导入用户: {csv_file}")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            imported_count = 0
            
            for row in reader:
                username = row.get('username', '').strip()
                password = row.get('password', '123456').strip()
                name = row.get('name', '').strip()
                role = row.get('role', 'student').strip()
                email = row.get('email', '').strip()
                
                if not username:
                    print(f"  跳过无效行: 缺少用户名")
                    continue
                
                # 检查用户是否已存在
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    print(f"  用户已存在: {username}")
                    continue
                
                # 插入新用户
                password_hash = hash_password(password)
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO users 
                    (username, password_hash, name, role, email, created_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (username, password_hash, name, role, email, created_at, True))
                
                imported_count += 1
                print(f"  导入用户: {username} ({name})")
            
            conn.commit()
            print(f"[OK] 成功导入 {imported_count} 个用户")
            
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")
    finally:
        conn.close()

def import_problems_from_csv(csv_file):
    """从CSV文件导入题目"""
    print(f"从CSV文件导入题目: {csv_file}")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            imported_count = 0
            
            for row in reader:
                title = row.get('title', '').strip()
                description = row.get('description', '').strip()
                difficulty = row.get('difficulty', 'easy').strip()
                score = int(row.get('score', 10))
                time_limit = int(row.get('time_limit', 1000))
                memory_limit = int(row.get('memory_limit', 256))
                tags = row.get('tags', '').strip()
                is_public = row.get('is_public', 'true').strip().lower() == 'true'
                
                if not title:
                    print(f"  跳过无效行: 缺少标题")
                    continue
                
                # 检查题目是否已存在
                cursor.execute("SELECT id FROM problems WHERE title = ?", (title,))
                if cursor.fetchone():
                    print(f"  题目已存在: {title}")
                    continue
                
                # 插入新题目
                created_by = 2  # test_teacher的用户ID
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO problems 
                    (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public))
                
                imported_count += 1
                print(f"  导入题目: {title} ({difficulty})")
            
            conn.commit()
            print(f"[OK] 成功导入 {imported_count} 个题目")
            
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")
    finally:
        conn.close()

def import_classes_from_csv(csv_file):
    """从CSV文件导入班级"""
    print(f"从CSV文件导入班级: {csv_file}")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            imported_count = 0
            
            for row in reader:
                name = row.get('name', '').strip()
                description = row.get('description', '').strip()
                teacher_id = int(row.get('teacher_id', 2))  # 默认test_teacher
                
                if not name:
                    print(f"  跳过无效行: 缺少班级名称")
                    continue
                
                # 检查班级是否已存在
                cursor.execute("SELECT id FROM classes WHERE name = ?", (name,))
                if cursor.fetchone():
                    print(f"  班级已存在: {name}")
                    continue
                
                # 插入新班级
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO classes 
                    (name, description, teacher_id, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (name, description, teacher_id, created_at))
                
                imported_count += 1
                print(f"  导入班级: {name}")
            
            conn.commit()
            print(f"[OK] 成功导入 {imported_count} 个班级")
            
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")
    finally:
        conn.close()

def export_data_to_json():
    """导出数据到JSON文件"""
    print("导出数据到JSON文件...")
    
    conn = sqlite3.connect('codeedu.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {}
    
    try:
        # 导出用户
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        data['users'] = users
        print(f"  导出 {len(users)} 个用户")
        
        # 导出题目
        cursor.execute("SELECT * FROM problems")
        problems = [dict(row) for row in cursor.fetchall()]
        data['problems'] = problems
        print(f"  导出 {len(problems)} 个题目")
        
        # 导出比赛
        cursor.execute("SELECT * FROM contests")
        contests = [dict(row) for row in cursor.fetchall()]
        data['contests'] = contests
        print(f"  导出 {len(contests)} 个比赛")
        
        # 导出班级
        cursor.execute("SELECT * FROM classes")
        classes = [dict(row) for row in cursor.fetchall()]
        data['classes'] = classes
        print(f"  导出 {len(classes)} 个班级")
        
        # 保存到文件
        with open('codeedu_export.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("[OK] 数据导出完成: codeedu_export.json")
        
    except Exception as e:
        print(f"[ERROR] 导出失败: {e}")
    finally:
        conn.close()

def show_usage():
    """显示使用说明"""
    print("""
数据导入工具使用说明:

1. 导入用户:
   python data_import_tool.py import_users users.csv

2. 导入题目:
   python data_import_tool.py import_problems problems.csv

3. 导入班级:
   python data_import_tool.py import_classes classes.csv

4. 导出所有数据:
   python data_import_tool.py export

5. 显示使用说明:
   python data_import_tool.py help

CSV文件格式示例:

用户CSV (users.csv):
  username,password,name,role,email
  student1,123456,学生1,student,student1@example.com
  teacher1,123456,教师1,teacher,teacher1@example.com

题目CSV (problems.csv):
  title,description,difficulty,score,time_limit,memory_limit,tags,is_public
  两数之和,给定一个整数数组...,easy,10,1000,256,数组,哈希表,true
  反转链表,反转一个单链表...,medium,15,2000,512,链表,true

班级CSV (classes.csv):
  name,description,teacher_id
  计算机科学2026,计算机科学专业班级,2
  软件工程2026,软件工程专业班级,2
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "import_users" and len(sys.argv) >= 3:
        import_users_from_csv(sys.argv[2])
    elif command == "import_problems" and len(sys.argv) >= 3:
        import_problems_from_csv(sys.argv[2])
    elif command == "import_classes" and len(sys.argv) >= 3:
        import_classes_from_csv(sys.argv[2])
    elif command == "export":
        export_data_to_json()
    elif command == "help":
        show_usage()
    else:
        print("[ERROR] 无效命令")
        show_usage()
