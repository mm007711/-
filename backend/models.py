from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# 用户表
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # 'student', 'teacher', 'admin'
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # 关系
    submissions = relationship("Submission", back_populates="user")
    contest_participations = relationship("ContestParticipation", back_populates="user")

# 题目表
class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # 'easy', 'medium', 'hard'
    score = Column(Integer, default=10)
    time_limit = Column(Integer, default=1000)  # 毫秒
    memory_limit = Column(Integer, default=256)  # MB
    tags = Column(String(255))  # 逗号分隔的标签
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    is_public = Column(Boolean, default=True)
    
    # 关系
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem")
    contest_problems = relationship("ContestProblem", back_populates="problem")

# 测试用例表
class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    
    # 关系
    problem = relationship("Problem", back_populates="test_cases")

# 比赛表
class Contest(Base):
    __tablename__ = "contests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_public = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    problems = relationship("ContestProblem", back_populates="contest", cascade="all, delete-orphan")
    participations = relationship("ContestParticipation", back_populates="contest", cascade="all, delete-orphan")

# 比赛-题目关联表
class ContestProblem(Base):
    __tablename__ = "contest_problems"
    
    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    order = Column(Integer, default=0)
    score = Column(Integer, default=10)
    
    # 关系
    contest = relationship("Contest", back_populates="problems")
    problem = relationship("Problem", back_populates="contest_problems")

# 比赛参与表
class ContestParticipation(Base):
    __tablename__ = "contest_participations"
    
    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=func.now())
    total_score = Column(Integer, default=0)
    total_time = Column(Integer, default=0)  # 秒
    
    # 关系
    contest = relationship("Contest", back_populates="participations")
    user = relationship("User", back_populates="contest_participations")

# 提交表
class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    contest_id = Column(Integer, ForeignKey("contests.id"), nullable=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)  # 'python', 'javascript', 'cpp'
    status = Column(String(20), default="pending")  # 'pending', 'judging', 'accepted', 'wrong_answer', 'time_limit_exceeded', 'runtime_error', 'compilation_error'
    score = Column(Integer, default=0)
    time_used = Column(Integer)  # 毫秒
    memory_used = Column(Integer)  # KB
    submitted_at = Column(DateTime, default=func.now())
    judged_at = Column(DateTime)
    
    # 关系
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
    test_results = relationship("TestResult", back_populates="submission", cascade="all, delete-orphan")

# 测试结果表
class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)
    status = Column(String(20), nullable=False)  # 'accepted', 'wrong_answer', 'time_limit_exceeded', 'runtime_error'
    time_used = Column(Integer)  # 毫秒
    memory_used = Column(Integer)  # KB
    output = Column(Text)
    
    # 关系
    submission = relationship("Submission", back_populates="test_results")
    test_case = relationship("TestCase")

# 班级表
class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    enrollments = relationship("ClassEnrollment", back_populates="class_", cascade="all, delete-orphan")

# 班级注册表
class ClassEnrollment(Base):
    __tablename__ = "class_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enrolled_at = Column(DateTime, default=func.now())
    score = Column(Integer, default=0)
    solved_count = Column(Integer, default=0)
    
    # 关系
    class_ = relationship("Class", back_populates="enrollments")
    student = relationship("User")
