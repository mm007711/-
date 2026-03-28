#!/usr/bin/env python3
"""
初始化测试数据脚本
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
                name="测试学生",
                role="student",
                email="student@test.com"
            ),
            User(
                username="test_teacher",
                password_hash=hash_password("test123"),
                name="测试教师",
                role="teacher",
                email="teacher@test.com"
            ),
            User(
                username="test_admin",
                password_hash=hash_password("test123"),
                name="测试管理员",
                role="admin",
                email="admin@test.com"
            )
        ]
        
        for user in users:
            existing = db.query(User).filter(User.username == user.username).first()
            if not existing:
                db.add(user)
        
        db.commit()
        print("创建测试用户")
        
        # 2. 创建测试题目
        teacher = db.query(User).filter(User.username == "test_teacher").first()
        if teacher:
            problems = [
                Problem(
                    title="两数之和",
                    description="给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回它们的数组下标。\n\n你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。",
                    difficulty="easy",
                    score=10,
                    time_limit=1000,
                    memory_limit=256,
                    tags="数组,哈希表",
                    created_by=teacher.id,
                    is_public=True
                ),
                Problem(
                    title="有效的括号",
                    description="给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。\n\n有效字符串需满足：\n1. 左括号必须用相同类型的右括号闭合。\n2. 左括号必须以正确的顺序闭合。",
                    difficulty="easy",
                    score=10,
                    time_limit=1000,
                    memory_limit=256,
                    tags="栈,字符串",
                    created_by=teacher.id,
                    is_public=True
                ),
                Problem(
                    title="合并两个有序链表",
                    description="将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。",
                    difficulty="medium",
                    score=20,
                    time_limit=2000,
                    memory_limit=256,
                    tags="链表,递归",
                    created_by=teacher.id,
                    is_public=True
                )
            ]
            
            for problem in problems:
                existing = db.query(Problem).filter(Problem.title == problem.title).first()
                if not existing:
                    db.add(problem)
            
            db.commit()
            print("创建测试题目")
            
            # 3. 为第一个题目创建测试用例
            problem1 = db.query(Problem).filter(Problem.title == "两数之和").first()
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
                print("✓ 创建测试用例")
            
            # 4. 创建测试比赛
            now = datetime.utcnow()
            contests = [
                Contest(
                    title="春季编程大赛",
                    description="年度春季编程大赛，包含各种难度题目",
                    start_time=now + timedelta(days=1),
                    end_time=now + timedelta(days=2),
                    is_public=True,
                    created_by=teacher.id
                ),
                Contest(
                    title="周赛 #1",
                    description="每周例行比赛",
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
            print("✓ 创建测试比赛")
            
            # 5. 创建测试班级
            classes = [
                Class(
                    name="计算机科学2026班",
                    description="计算机科学专业2026级学生",
                    teacher_id=teacher.id
                ),
                Class(
                    name="软件工程2026班",
                    description="软件工程专业2026级学生",
                    teacher_id=teacher.id
                )
            ]
            
            for class_ in classes:
                existing = db.query(Class).filter(Class.name == class_.name).first()
                if not existing:
                    db.add(class_)
            
            db.commit()
            print("✓ 创建测试班级")
            
            # 6. 注册学生到班级
            student = db.query(User).filter(User.username == "test_student").first()
            class1 = db.query(Class).filter(Class.name == "计算机科学2026班").first()
            
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
                    print("✓ 注册学生到班级")
        
        print("\n✅ 测试数据初始化完成！")
        print("\n可用测试账户：")
        print("  学生: test_student / test123")
        print("  教师: test_teacher / test123")
        print("  管理员: test_admin / test123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("正在初始化数据库和测试数据...")
    init_db()  # 确保数据库表已创建
    create_test_data()
