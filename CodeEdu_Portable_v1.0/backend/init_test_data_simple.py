#!/usr/bin/env python3
"""
初始化测试数据脚本 - 简单版本
"""

import sys
import os
import hashlib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import User, Problem, TestCase, Contest, Class, ClassEnrollment
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    """简单的密码哈希函数"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    
    try:
        # 1. 创建测试用户
        users = [
            User(
                username="test_student",
                password_hash=hash_password("test123"),
                name="Test Student",
                role="student",
                email="student@test.com"
            ),
            User(
                username="test_teacher",
                password_hash=hash_password("test123"),
                name="Test Teacher",
                role="teacher",
                email="teacher@test.com"
            ),
            User(
                username="test_admin",
                password_hash=hash_password("test123"),
                name="Test Admin",
                role="admin",
                email="admin@test.com"
            )
        ]
        
        for user in users:
            existing = db.query(User).filter(User.username == user.username).first()
            if not existing:
                db.add(user)
        
        db.commit()
        print("Created test users")
        
        # 2. 创建测试题目
        teacher = db.query(User).filter(User.username == "test_teacher").first()
        if teacher:
            problems = [
                Problem(
                    title="Two Sum",
                    description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                    difficulty="easy",
                    score=10,
                    time_limit=1000,
                    memory_limit=256,
                    tags="array,hash",
                    created_by=teacher.id,
                    is_public=True
                ),
                Problem(
                    title="Valid Parentheses",
                    description="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                    difficulty="easy",
                    score=10,
                    time_limit=1000,
                    memory_limit=256,
                    tags="stack,string",
                    created_by=teacher.id,
                    is_public=True
                ),
                Problem(
                    title="Merge Two Sorted Lists",
                    description="Merge two sorted linked lists and return it as a sorted list.",
                    difficulty="medium",
                    score=20,
                    time_limit=2000,
                    memory_limit=256,
                    tags="linked list,recursion",
                    created_by=teacher.id,
                    is_public=True
                )
            ]
            
            for problem in problems:
                existing = db.query(Problem).filter(Problem.title == problem.title).first()
                if not existing:
                    db.add(problem)
            
            db.commit()
            print("Created test problems")
            
            # 3. 为第一个题目创建测试用例
            problem1 = db.query(Problem).filter(Problem.title == "Two Sum").first()
            if problem1:
                test_cases = [
                    TestCase(
                        problem_id=problem1.id,
                        input_data="[2,7,11,15]\n9",
                        expected_output="[0,1]",
                        is_sample=True,
                        order=1
                    ),
                    TestCase(
                        problem_id=problem1.id,
                        input_data="[3,2,4]\n6",
                        expected_output="[1,2]",
                        is_sample=False,
                        order=2
                    ),
                    TestCase(
                        problem_id=problem1.id,
                        input_data="[3,3]\n6",
                        expected_output="[0,1]",
                        is_sample=False,
                        order=3
                    )
                ]
                
                for test_case in test_cases:
                    existing = db.query(TestCase).filter(
                        TestCase.problem_id == test_case.problem_id,
                        TestCase.input_data == test_case.input_data
                    ).first()
                    if not existing:
                        db.add(test_case)
                
                db.commit()
                print("Created test cases")
            
            # 4. 创建测试比赛
            now = datetime.utcnow()
            contests = [
                Contest(
                    title="Spring Programming Contest",
                    description="Annual spring programming contest",
                    start_time=now + timedelta(days=1),
                    end_time=now + timedelta(days=2),
                    is_public=True,
                    created_by=teacher.id
                ),
                Contest(
                    title="Weekly Contest #1",
                    description="Weekly programming contest",
                    start_time=now - timedelta(hours=1),
                    end_time=now + timedelta(hours=2),
                    is_public=True,
                    created_by=teacher.id
                )
            ]
            
            for contest in contests:
                existing = db.query(Contest).filter(Contest.title == contest.title).first()
                if not existing:
                    db.add(contest)
            
            db.commit()
            print("Created test contests")
            
            # 5. 创建测试班级
            classes = [
                Class(
                    name="Computer Science 2026",
                    description="Computer Science class 2026",
                    teacher_id=teacher.id
                ),
                Class(
                    name="Software Engineering 2026",
                    description="Software Engineering class 2026",
                    teacher_id=teacher.id
                )
            ]
            
            for class_ in classes:
                existing = db.query(Class).filter(Class.name == class_.name).first()
                if not existing:
                    db.add(class_)
            
            db.commit()
            print("Created test classes")
            
            # 6. 注册学生到班级
            student = db.query(User).filter(User.username == "test_student").first()
            class1 = db.query(Class).filter(Class.name == "Computer Science 2026").first()
            
            if student and class1:
                enrollment = ClassEnrollment(
                    class_id=class1.id,
                    student_id=student.id,
                    score=85,
                    solved_count=5
                )
                
                existing = db.query(ClassEnrollment).filter(
                    ClassEnrollment.class_id == class1.id,
                    ClassEnrollment.student_id == student.id
                ).first()
                
                if not existing:
                    db.add(enrollment)
                    db.commit()
                    print("Enrolled student to class")
        
        print("\nTest data initialization completed!")
        print("\nTest accounts:")
        print("  Student: test_student / test123")
        print("  Teacher: test_teacher / test123")
        print("  Admin: test_admin / test123")
        
    except Exception as e:
        db.rollback()
        print(f"Initialization failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database and test data...")
    init_db()  # 确保数据库表已创建
    create_test_data()
