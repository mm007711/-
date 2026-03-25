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
    db_path = os.path.join(os.path.dirname(__file__), '..', 'codeedu.db')
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
    problem_id = request.args.get('problem_id', '4')
    code = data.get('code', '')
    
    # 模拟评测结果
    result = {
        'status': 'AC',
        'report': '全部用例通过（模拟）。',
        'score': 10,
        'total_cases': 3,
        'passed_cases': 3,
        'cases': [
            {'caseId': 1, 'input': '2 7 11 15,9', 'expected': '[0,1]', 'actual': '[0,1]', 'status': 'AC', 'runtimeMs': 12.3},
            {'caseId': 2, 'input': '3 2 4,6', 'expected': '[1,2]', 'actual': '[1,2]', 'status': 'AC', 'runtimeMs': 10.1},
            {'caseId': 3, 'input': '3 3,6', 'expected': '[0,1]', 'actual': '[0,1]', 'status': 'AC', 'runtimeMs': 9.4},
        ]
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
