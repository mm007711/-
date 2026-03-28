#!/usr/bin/env python3
"""
增强版数据导入工具 - 支持CSV/Excel/手动添加
"""

import sqlite3
import csv
import json
import datetime
import hashlib
import sys
import os
from pathlib import Path

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def import_users_from_excel(excel_file):
    """从Excel文件导入用户"""
    print(f"从Excel文件导入用户: {excel_file}")
    
    try:
        # 尝试导入pandas库
        import pandas as pd
        
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        print(f"  读取到 {len(df)} 行数据")
        
        conn = sqlite3.connect('codeedu.db')
        cursor = conn.cursor()
        
        imported_count = 0
        for _, row in df.iterrows():
            username = str(row.get('username', '')).strip()
            password = str(row.get('password', '123456')).strip()
            name = str(row.get('name', '')).strip()
            role = str(row.get('role', 'student')).strip()
            email = str(row.get('email', '')).strip()
            
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
        conn.close()
        print(f"[OK] 成功导入 {imported_count} 个用户")
        
    except ImportError:
        print("[ERROR] 需要安装pandas库: pip install pandas openpyxl")
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")

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

def import_problems_from_excel(excel_file):
    """从Excel文件导入题目"""
    print(f"从Excel文件导入题目: {excel_file}")
    
    try:
        import pandas as pd
        
        df = pd.read_excel(excel_file)
        print(f"  读取到 {len(df)} 行数据")
        
        conn = sqlite3.connect('codeedu.db')
        cursor = conn.cursor()
        
        imported_count = 0
        for _, row in df.iterrows():
            title = str(row.get('title', '')).strip()
            description = str(row.get('description', '')).strip()
            difficulty = str(row.get('difficulty', 'easy')).strip()
            score = int(row.get('score', 10))
            time_limit = int(row.get('time_limit', 1000))
            memory_limit = int(row.get('memory_limit', 256))
            tags = str(row.get('tags', '')).strip()
            is_public = str(row.get('is_public', 'true')).strip().lower() == 'true'
            
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
        conn.close()
        print(f"[OK] 成功导入 {imported_count} 个题目")
        
    except ImportError:
        print("[ERROR] 需要安装pandas库: pip install pandas openpyxl")
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")

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

def import_classes_from_excel(excel_file):
    """从Excel文件导入班级"""
    print(f"从Excel文件导入班级: {excel_file}")
    
    try:
        import pandas as pd
        
        df = pd.read_excel(excel_file)
        print(f"  读取到 {len(df)} 行数据")
        
        conn = sqlite3.connect('codeedu.db')
        cursor = conn.cursor()
        
        imported_count = 0
        for _, row in df.iterrows():
            name = str(row.get('name', '')).strip()
            description = str(row.get('description', '')).strip()
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
        conn.close()
        print(f"[OK] 成功导入 {imported_count} 个班级")
        
    except ImportError:
        print("[ERROR] 需要安装pandas库: pip install pandas openpyxl")
    except Exception as e:
        print(f"[ERROR] 导入失败: {e}")

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

def manual_add_user():
    """手动添加用户"""
    print("=== 手动添加用户 ===")
    
    username = input("用户名: ").strip()
    if not username:
        print("[ERROR] 用户名不能为空")
        return
    
    password = input("密码 (默认: 123456): ").strip() or "123456"
    name = input("姓名: ").strip()
    role = input("角色 (student/teacher, 默认: student): ").strip() or "student"
    email = input("邮箱 (可选): ").strip()
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        # 检查用户是否已存在
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"[ERROR] 用户已存在: {username}")
            return
        
        # 插入新用户
        password_hash = hash_password(password)
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO users 
            (username, password_hash, name, role, email, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, name, role, email, created_at, True))
        
        conn.commit()
        print(f"[OK] 成功添加用户: {username} ({name})")
        
    except Exception as e:
        print(f"[ERROR] 添加失败: {e}")
    finally:
        conn.close()

def manual_add_problem():
    """手动添加题目"""
    print("=== 手动添加题目 ===")
    
    title = input("题目标题: ").strip()
    if not title:
        print("[ERROR] 题目标题不能为空")
        return
    
    description = input("题目描述: ").strip()
    difficulty = input("难度 (easy/medium/hard, 默认: easy): ").strip() or "easy"
    score = int(input("分值 (默认: 10): ").strip() or "10")
    time_limit = int(input("时间限制(ms) (默认: 1000): ").strip() or "1000")
    memory_limit = int(input("内存限制(MB) (默认: 256): ").strip() or "256")
    tags = input("标签 (用逗号分隔): ").strip()
    is_public = input("是否公开 (true/false, 默认: true): ").strip().lower() == 'true'
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        # 检查题目是否已存在
        cursor.execute("SELECT id FROM problems WHERE title = ?", (title,))
        if cursor.fetchone():
            print(f"[ERROR] 题目已存在: {title}")
            return
        
        # 插入新题目
        created_by = 2  # test_teacher的用户ID
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO problems 
            (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public))
        
        conn.commit()
        print(f"[OK] 成功添加题目: {title} ({difficulty})")
        
    except Exception as e:
        print(f"[ERROR] 添加失败: {e}")
    finally:
        conn.close()

def manual_add_class():
    """手动添加班级"""
    print("=== 手动添加班级 ===")
    
    name = input("班级名称: ").strip()
    if not name:
        print("[ERROR] 班级名称不能为空")
        return
    
    description = input("班级描述: ").strip()
    teacher_id = int(input("教师ID (默认: 2): ").strip() or "2")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    try:
        # 检查班级是否已存在
        cursor.execute("SELECT id FROM classes WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"[ERROR] 班级已存在: {name}")
            return
        
        # 插入新班级
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO classes 
            (name, description, teacher_id, created_at)
            VALUES (?, ?, ?, ?)
        ''', (name, description, teacher_id, created_at))
        
        conn.commit()
        print(f"[OK] 成功添加班级: {name}")
        
    except Exception as e:
        print(f"[ERROR] 添加失败: {e}")
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
增强版数据导入工具使用说明:

1. 导入用户:
   python data_import_tool_enhanced.py import_users users.csv
   python data_import_tool_enhanced.py import_users_excel users.xlsx

2. 导入题目:
   python data_import_tool_enhanced.py import_problems problems.csv
   python data_import_tool_enhanced.py import_problems_excel problems.xlsx

3. 导入班级:
   python data_import_tool_enhanced.py import_classes classes.csv
   python data_import_tool_enhanced.py import_classes_excel classes.xlsx

4. 手动添加:
   python data_import_tool_enhanced.py manual_add_user
   python data_import_tool_enhanced.py manual_add_problem
   python data_import_tool_enhanced.py manual_add_class

5. 导出所有数据:
   python data_import_tool_enhanced.py export

6. 显示使用说明:
   python data_import_tool_enhanced.py help

文件格式示例:

用户Excel/CSV:
  username,password,name,role,email
  student1,123456,学生1,student,student1@example.com
  teacher1,123456,教师1,teacher,teacher1@example.com

题目Excel/CSV:
  title,description,difficulty,score,time_limit,memory_limit,tags,is_public
  两数之和,给定一个整数数组...,easy,10,1000,256,数组,哈希表,true
  反转链表,反转一个单链表...,medium,15,2000,512,链表,true

班级Excel/CSV:
  name,description,teacher_id
  计算机科学2026,计算机科学专业班级,2
  软件工程2026,软件工程专业班级,2

注意: 使用Excel功能需要安装pandas和openpyxl:
  pip install pandas openpyxl
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "import_users" and len(sys.argv) >= 3:
        import_users_from_csv(sys.argv[2])
    elif command == "import_users_excel" and len(sys.argv) >= 3:
        import_users_from_excel(sys.argv[2])
    elif command == "import_problems" and len(sys.argv) >= 3:
        import_problems_from_csv(sys.argv[2])
    elif command == "import_problems_excel" and len(sys.argv) >= 3:
        import_problems_from_excel(sys.argv[2])
    elif command == "import_classes" and len(sys.argv) >= 3:
        import_classes_from_csv(sys.argv[2])
    elif command == "import_classes_excel" and len(sys.argv) >= 3:
        import_classes_from_excel(sys.argv[2])
    elif command == "manual_add_user":
        manual_add_user()
    elif command == "manual_add_problem":
        manual_add_problem()
    elif command == "manual_add_class":
        manual_add_class()
    elif command == "export":
        export_data_to_json()
    elif command == "help":
        show_usage()
    else:
        print("[ERROR] 无效命令")
        show_usage()
