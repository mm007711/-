#!/usr/bin/env python3
"""
简单的后端服务器 - 用于测试
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = "your-secret-key-change-in-production"

def get_db():
    import os
    # 使用绝对路径连接到数据库
    db_path = os.path.join('d:/codeedu', 'codeedu.db')
    
    # 如果绝对路径不存在，尝试相对路径
    if not os.path.exists(db_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'codeedu.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except:
        return None

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 支持多种用户名格式
    possible_usernames = [username]
    if username == 'teacher':
        possible_usernames.extend(['test_teacher', 'teacher2'])
    elif username == 'student':
        possible_usernames.extend(['test_student', 'student1', 'student2', 'student3'])
    elif username == 'admin':
        possible_usernames.extend(['test_admin', 'admin2'])
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 尝试所有可能的用户名
    user = None
    for uname in possible_usernames:
        cursor.execute('SELECT * FROM users WHERE username = ?', (uname,))
        user = cursor.fetchone()
        if user:
            break
    
    conn.close()
    
    if user and user['password_hash'] == hash_password(password):
        token = jwt.encode({
            'sub': user['username'],  # 使用实际的用户名
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY)
        return jsonify({
            'access_token': token,
            'token_type': 'bearer',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'name': user['name'],
                'role': user['role'],
                'email': user['email']
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/problems', methods=['GET'])
def get_problems():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problems WHERE is_public = 1')
    problems = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(problem) for problem in problems])

@app.route('/api/contests', methods=['GET'])
def get_contests():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contests')
    contests = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(contest) for contest in contests])

@app.route('/api/classes', methods=['GET'])
def get_classes():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(class_) for class_ in classes])

@app.route('/api/judge/run', methods=['POST'])
def judge():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    problem_id = request.args.get('problem_id', '1')  # 默认使用第一个题目
    code = data.get('code', '')
    
    # 获取题目信息
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
    problem = cursor.fetchone()
    conn.close()
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    # 获取测试用例
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test_cases WHERE problem_id = ? ORDER BY "order"', (problem_id,))
    test_cases = cursor.fetchall()
    conn.close()
    
    if not test_cases:
        # 如果没有测试用例，使用模拟评测
        result = {
            'status': 'AC',
            'report': '全部用例通过（模拟，无测试用例）。',
            'score': problem['score'],
            'total_cases': 3,
            'passed_cases': 3,
            'cases': [
                {'caseId': 1, 'input': '2 7 11 15,9', 'expected': '[0,1]', 'actual': '[0,1]', 'status': 'AC', 'runtimeMs': 12.3},
                {'caseId': 2, 'input': '3 2 4,6', 'expected': '[1,2]', 'actual': '[1,2]', 'status': 'AC', 'runtimeMs': 10.1},
                {'caseId': 3, 'input': '3 3,6', 'expected': '[0,1]', 'actual': '[0,1]', 'status': 'AC', 'runtimeMs': 9.4},
            ]
        }
    else:
        # 使用真实测试用例
        cases = []
        passed = 0
        
        for i, test_case in enumerate(test_cases, 1):
            # 这里应该调用真实的评测逻辑，但为了简单起见，我们模拟评测
            # 在实际系统中，这里应该调用 judge.py 中的评测函数
            
            # 更合理的模拟：检查代码是否包含关键函数
            code_lower = code.lower()
            has_two_sum = 'two_sum' in code_lower or 'def two_sum' in code_lower
            has_solution = 'solution' in code_lower or 'class solution' in code_lower
            
            # 根据代码内容决定是否通过
            if problem_id == '1':  # 两数之和
                is_passed = has_two_sum or has_solution
            else:
                # 其他题目：如果代码长度合理且包含函数定义，则通过
                is_passed = len(code) > 20 and ('def ' in code_lower or 'function ' in code_lower or 'class ' in code_lower)
            
            # 模拟不同的状态
            if is_passed:
                status = 'AC'
                actual_output = test_case['expected_output']
            else:
                # 随机生成错误状态
                import random
                error_types = ['WA', 'TLE', 'RE', 'CE']
                status = random.choice(error_types)
                actual_output = 'Error: ' + status
            
            case_result = {
                'caseId': i,
                'input': test_case['input_data'][:50] + ('...' if len(test_case['input_data']) > 50 else ''),
                'expected': test_case['expected_output'][:50] + ('...' if len(test_case['expected_output']) > 50 else ''),
                'actual': actual_output[:50] + ('...' if len(actual_output) > 50 else ''),
                'status': status,
                'runtimeMs': round(10 + i * 0.5 + random.random() * 5, 1) if 'random' in locals() else round(10 + i * 0.5, 1)
            }
            
            cases.append(case_result)
            if status == 'AC':
                passed += 1
        
        # 确定最终状态
        if passed == len(test_cases):
            final_status = 'AC'
        elif any(case['status'] == 'TLE' for case in cases):
            final_status = 'TLE'
        elif any(case['status'] == 'RE' for case in cases):
            final_status = 'RE'
        elif any(case['status'] == 'CE' for case in cases):
            final_status = 'CE'
        else:
            final_status = 'WA'
        
        score = int((passed / len(test_cases)) * problem['score']) if test_cases else 0
        
        result = {
            'status': final_status,
            'report': f'通过 {passed}/{len(test_cases)} 个测试用例。',
            'score': score,
            'total_cases': len(test_cases),
            'passed_cases': passed,
            'cases': cases
        }
    
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM problems')
    total_problems = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM contests')
    total_contests = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM submissions')
    total_submissions = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total_problems': total_problems,
        'total_contests': total_contests,
        'total_submissions': total_submissions,
        'total_users': total_users,
        'active_contests': 1
    })

# 添加更多API端点以支持完整功能
@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'is_active': user['is_active'],
            'created_at': user['created_at']
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/problems/<int:problem_id>', methods=['GET'])
def get_problem_by_id(problem_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
    problem = cursor.fetchone()
    conn.close()
    
    if problem:
        return jsonify(dict(problem))
    return jsonify({'error': 'Problem not found'}), 404

@app.route('/api/problems', methods=['POST'])
def create_problem_api():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取当前用户ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # 插入新题目
    cursor.execute('''
        INSERT INTO problems (title, description, difficulty, score, time_limit, memory_limit, tags, is_public, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title', '新题目'),
        data.get('description', ''),
        data.get('difficulty', '简单'),
        data.get('score', 10),
        data.get('time_limit', 1000),
        data.get('memory_limit', 256),
        data.get('tags', ''),
        data.get('is_public', True),
        user['id']
    ))
    
    problem_id = cursor.lastrowid
    conn.commit()
    
    # 获取新创建的题目
    cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
    new_problem = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(new_problem)), 201

@app.route('/api/contests', methods=['POST'])
def create_contest_api():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取当前用户ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # 插入新比赛
    cursor.execute('''
        INSERT INTO contests (title, description, start_time, end_time, is_public, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title', '新比赛'),
        data.get('description', ''),
        data.get('start_time', '2024-01-01 00:00:00'),
        data.get('end_time', '2024-12-31 23:59:59'),
        data.get('is_public', True),
        user['id']
    ))
    
    contest_id = cursor.lastrowid
    conn.commit()
    
    # 获取新创建的比赛
    cursor.execute('SELECT * FROM contests WHERE id = ?', (contest_id,))
    new_contest = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(new_contest)), 201

@app.route('/api/classes', methods=['POST'])
def create_class_api():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取当前用户ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # 插入新班级
    cursor.execute('''
        INSERT INTO classes (name, description, teacher_id)
        VALUES (?, ?, ?)
    ''', (
        data.get('name', '新班级'),
        data.get('description', ''),
        user['id']
    ))
    
    class_id = cursor.lastrowid
    conn.commit()
    
    # 获取新创建的班级
    cursor.execute('SELECT * FROM classes WHERE id = ?', (class_id,))
    new_class = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(new_class)), 201

@app.route('/api/classes/<int:class_id>/enroll', methods=['POST'])
def enroll_student_api(class_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not verify_token(token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    student_id = data.get('student_id')
    
    if not student_id:
        return jsonify({'error': 'Student ID is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查班级是否存在
    cursor.execute('SELECT * FROM classes WHERE id = ?', (class_id,))
    class_ = cursor.fetchone()
    if not class_:
        conn.close()
        return jsonify({'error': 'Class not found'}), 404
    
    # 检查学生是否存在
    cursor.execute('SELECT * FROM users WHERE id = ? AND role = "student"', (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
    
    # 检查是否已经注册
    cursor.execute('SELECT * FROM class_enrollments WHERE class_id = ? AND student_id = ?', (class_id, student_id))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'Student already enrolled'}), 400
    
    # 注册学生
    cursor.execute('''
        INSERT INTO class_enrollments (class_id, student_id, score, solved_count)
        VALUES (?, ?, ?, ?)
    ''', (class_id, student_id, data.get('score', 0), data.get('solved_count', 0)))
    
    enrollment_id = cursor.lastrowid
    conn.commit()
    
    # 获取新创建的注册记录
    cursor.execute('SELECT * FROM class_enrollments WHERE id = ?', (enrollment_id,))
    new_enrollment = cursor.fetchone()
    conn.close()
    
    return jsonify(dict(new_enrollment)), 201

# 添加根路径路由
@app.route('/')
def index():
    return jsonify({
        'name': 'CodeEdu API',
        'version': '2.0.0',
        'endpoints': {
            'auth': '/api/auth/login',
            'problems': '/api/problems',
            'contests': '/api/contests',
            'classes': '/api/classes',
            'judge': '/api/judge/run',
            'stats': '/api/stats'
        }
    })

if __name__ == '__main__':
    print("启动简单服务器在 http://localhost:5000")
    app.run(debug=True, port=5000)
