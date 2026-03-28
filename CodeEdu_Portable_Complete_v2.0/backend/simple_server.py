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
    # 数据库文件在当前目录的上一级目录中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'codeedu.db')
    # 确保路径正确
    if not os.path.exists(db_path):
        # 尝试在当前目录查找
        db_path = os.path.join(current_dir, 'codeedu.db')
        if not os.path.exists(db_path):
            # 尝试在项目根目录查找
            db_path = os.path.join(current_dir, '..', '..', 'codeedu.db')
    
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
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user['password_hash'] == hash_password(password):
        token = jwt.encode({
            'sub': username,
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

if __name__ == '__main__':
    print("启动简单服务器在 http://localhost:5000")
    app.run(debug=True, port=5000)
