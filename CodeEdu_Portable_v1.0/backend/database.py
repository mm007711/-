from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
import os

# 数据库URL
DATABASE_URL = "sqlite:///./codeedu.db"

# 创建引擎
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # SQLite需要这个参数
    echo=True  # 设置为True可以看到SQL语句
)

# 创建SessionLocal类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖注入函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化数据库
def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 添加默认数据
    db = SessionLocal()
    try:
        # 检查是否已有管理员用户
        from models import User
        
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 需要先导入密码上下文
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            # 创建默认管理员用户
            admin_user = User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                name="系统管理员",
                role="admin",
                email="admin@codeedu.com"
            )
            db.add(admin_user)
            
            # 创建默认教师用户
            teacher_user = User(
                username="teacher",
                password_hash=pwd_context.hash("teacher123"),
                name="教师",
                role="teacher",
                email="teacher@codeedu.com"
            )
            db.add(teacher_user)
            
            # 创建默认学生用户
            student_user = User(
                username="student",
                password_hash=pwd_context.hash("student123"),
                name="学生",
                role="student",
                email="student@codeedu.com"
            )
            db.add(student_user)
            
            db.commit()
            print("默认用户创建成功")
    except Exception as e:
        print(f"初始化数据库时出错: {e}")
        db.rollback()
    finally:
        db.close()
