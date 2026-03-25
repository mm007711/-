from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 用户相关
class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# 题目相关
class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    score: int
    time_limit: int
    memory_limit: int
    tags: str
    is_public: bool = True

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# 测试用例相关
class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_sample: bool = False
    order: int = 0

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseResponse(TestCaseBase):
    id: int
    problem_id: int
    
    class Config:
        from_attributes = True

# 比赛相关
class ContestBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    is_public: bool = True

class ContestCreate(ContestBase):
    pass

class ContestResponse(ContestBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# 提交相关
class SubmissionBase(BaseModel):
    code: str
    language: str

class SubmissionCreate(SubmissionBase):
    problem_id: int
    contest_id: Optional[int] = None

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    contest_id: Optional[int]
    language: str
    status: str
    score: int
    time_used: Optional[int]
    memory_used: Optional[int]
    submitted_at: datetime
    judged_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 测试结果相关
class TestResultBase(BaseModel):
    test_case_id: int
    status: str
    time_used: Optional[int]
    memory_used: Optional[int]
    output: Optional[str]

class TestResultResponse(TestResultBase):
    id: int
    submission_id: int
    
    class Config:
        from_attributes = True

# 判题响应
class JudgeCase(BaseModel):
    case_id: int
    input: str
    expected: str
    actual: str
    status: str
    time_used: float
    memory_used: int

class JudgeResponse(BaseModel):
    status: str
    report: str
    score: int
    total_cases: int
    passed_cases: int
    cases: List[JudgeCase]

# 班级相关
class ClassBase(BaseModel):
    name: str
    description: Optional[str]

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    teacher_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClassEnrollmentBase(BaseModel):
    student_id: int
    score: int = 0
    solved_count: int = 0

class ClassEnrollmentCreate(ClassEnrollmentBase):
    pass

class ClassEnrollmentResponse(ClassEnrollmentBase):
    id: int
    class_id: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True

# 统计相关
class StatsResponse(BaseModel):
    total_problems: int
    total_contests: int
    total_submissions: int
    total_users: int
    active_contests: int
