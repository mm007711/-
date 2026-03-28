#!/usr/bin/env python3
"""
图形界面数据导入工具 - 为不会编程的用户设计
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sqlite3
import csv
import json
import datetime
import hashlib
import os
import sys
from pathlib import Path

class DataImportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeEdu 数据导入工具")
        self.root.geometry("800x600")
        
        # 设置样式
        self.setup_styles()
        
        # 创建主界面
        self.create_widgets()
        
        # 数据库路径
        self.db_path = 'd:/codeedu/codeedu.db'
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        self.root.configure(bg='#f0f0f0')
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="CodeEdu 教学平台数据导入工具", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 创建各个选项卡
        self.create_import_tab()
        self.create_manual_tab()
        self.create_export_tab()
        self.create_status_tab()
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="检查数据库连接", command=self.check_db_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def create_import_tab(self):
        """创建导入选项卡"""
        import_tab = ttk.Frame(self.notebook)
        self.notebook.add(import_tab, text="批量导入")
        
        # 用户导入
        user_frame = ttk.LabelFrame(import_tab, text="导入用户", padding="10")
        user_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(user_frame, text="选择用户文件 (CSV/Excel):").grid(row=0, column=0, sticky=tk.W)
        self.user_file_var = tk.StringVar()
        ttk.Entry(user_frame, textvariable=self.user_file_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(user_frame, text="浏览...", command=lambda: self.browse_file(self.user_file_var)).grid(row=0, column=2)
        ttk.Button(user_frame, text="导入用户", command=self.import_users).grid(row=0, column=3, padx=5)
        
        # 题目导入
        problem_frame = ttk.LabelFrame(import_tab, text="导入题目", padding="10")
        problem_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(problem_frame, text="选择题目文件 (CSV/Excel):").grid(row=0, column=0, sticky=tk.W)
        self.problem_file_var = tk.StringVar()
        ttk.Entry(problem_frame, textvariable=self.problem_file_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(problem_frame, text="浏览...", command=lambda: self.browse_file(self.problem_file_var)).grid(row=0, column=2)
        ttk.Button(problem_frame, text="导入题目", command=self.import_problems).grid(row=0, column=3, padx=5)
        
        # 班级导入
        class_frame = ttk.LabelFrame(import_tab, text="导入班级", padding="10")
        class_frame.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(class_frame, text="选择班级文件 (CSV/Excel):").grid(row=0, column=0, sticky=tk.W)
        self.class_file_var = tk.StringVar()
        ttk.Entry(class_frame, textvariable=self.class_file_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(class_frame, text="浏览...", command=lambda: self.browse_file(self.class_file_var)).grid(row=0, column=2)
        ttk.Button(class_frame, text="导入班级", command=self.import_classes).grid(row=0, column=3, padx=5)
        
        # 文件格式说明
        help_frame = ttk.LabelFrame(import_tab, text="文件格式说明", padding="10")
        help_frame.grid(row=3, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        help_text = """CSV/Excel文件格式:
        
用户文件: username,password,name,role,email
示例: student1,123456,张三,student,zhangsan@example.com

题目文件: title,description,difficulty,score,time_limit,memory_limit,tags,is_public
示例: 两数之和,给定一个整数数组...,easy,10,1000,256,数组;哈希表,true

班级文件: name,description,teacher_id
示例: 计算机科学2026,计算机科学专业班级,2

注意: 所有文件应为UTF-8编码"""
        
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT)
        help_label.grid(row=0, column=0, sticky=tk.W)
        
        # 配置权重
        import_tab.columnconfigure(0, weight=1)
        for i in range(4):
            import_tab.rowconfigure(i, weight=1)
            
    def create_manual_tab(self):
        """创建手动添加选项卡"""
        manual_tab = ttk.Frame(self.notebook)
        self.notebook.add(manual_tab, text="手动添加")
        
        # 用户添加
        user_frame = ttk.LabelFrame(manual_tab, text="添加用户", padding="10")
        user_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(user_frame, text="用户名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.manual_username = ttk.Entry(user_frame, width=30)
        self.manual_username.grid(row=0, column=1, pady=5)
        
        ttk.Label(user_frame, text="密码:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.manual_password = ttk.Entry(user_frame, width=30, show="*")
        self.manual_password.grid(row=1, column=1, pady=5)
        self.manual_password.insert(0, "123456")
        
        ttk.Label(user_frame, text="姓名:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.manual_name = ttk.Entry(user_frame, width=30)
        self.manual_name.grid(row=2, column=1, pady=5)
        
        ttk.Label(user_frame, text="角色:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.manual_role = ttk.Combobox(user_frame, values=["student", "teacher", "admin"], width=28)
        self.manual_role.grid(row=3, column=1, pady=5)
        self.manual_role.set("student")
        
        ttk.Label(user_frame, text="邮箱:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.manual_email = ttk.Entry(user_frame, width=30)
        self.manual_email.grid(row=4, column=1, pady=5)
        
        ttk.Button(user_frame, text="添加用户", command=self.manual_add_user).grid(row=5, column=0, columnspan=2, pady=10)
        
        # 题目添加
        problem_frame = ttk.LabelFrame(manual_tab, text="添加题目", padding="10")
        problem_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(problem_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.manual_title = ttk.Entry(problem_frame, width=30)
        self.manual_title.grid(row=0, column=1, pady=5)
        
        ttk.Label(problem_frame, text="描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.manual_description = tk.Text(problem_frame, width=30, height=4)
        self.manual_description.grid(row=1, column=1, pady=5)
        
        ttk.Label(problem_frame, text="难度:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.manual_difficulty = ttk.Combobox(problem_frame, values=["easy", "medium", "hard"], width=28)
        self.manual_difficulty.grid(row=2, column=1, pady=5)
        self.manual_difficulty.set("easy")
        
        ttk.Label(problem_frame, text="分值:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.manual_score = ttk.Entry(problem_frame, width=30)
        self.manual_score.grid(row=3, column=1, pady=5)
        self.manual_score.insert(0, "10")
        
        ttk.Label(problem_frame, text="标签:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.manual_tags = ttk.Entry(problem_frame, width=30)
        self.manual_tags.grid(row=4, column=1, pady=5)
        
        ttk.Button(problem_frame, text="添加题目", command=self.manual_add_problem).grid(row=5, column=0, columnspan=2, pady=10)
        
        # 配置权重
        manual_tab.columnconfigure(0, weight=1)
        manual_tab.columnconfigure(1, weight=1)
        manual_tab.rowconfigure(0, weight=1)
        
    def create_export_tab(self):
        """创建导出选项卡"""
        export_tab = ttk.Frame(self.notebook)
        self.notebook.add(export_tab, text="数据导出")
        
        # 导出选项
        options_frame = ttk.LabelFrame(export_tab, text="导出选项", padding="10")
        options_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.export_users_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="导出用户", variable=self.export_users_var).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.export_problems_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="导出题目", variable=self.export_problems_var).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.export_classes_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="导出班级", variable=self.export_classes_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.export_contests_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="导出比赛", variable=self.export_contests_var).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        ttk.Button(options_frame, text="导出到JSON", command=self.export_to_json).grid(row=4, column=0, pady=10)
        ttk.Button(options_frame, text="导出到CSV", command=self.export_to_csv).grid(row=5, column=0, pady=10)
        
        # 导出路径
        path_frame = ttk.LabelFrame(export_tab, text="导出路径", padding="10")
        path_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(path_frame, text="导出文件路径:").grid(row=0, column=0, sticky=tk.W)
        self.export_path_var = tk.StringVar(value="codeedu_export.json")
        ttk.Entry(path_frame, textvariable=self.export_path_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(path_frame, text="浏览...", command=self.browse_export_path).grid(row=0, column=2)
        
        # 配置权重
        export_tab.columnconfigure(0, weight=1)
        export_tab.rowconfigure(0, weight=1)
        export_tab.rowconfigure(1, weight=1)
        
    def create_status_tab(self):
        """创建状态选项卡"""
        status_tab = ttk.Frame(self.notebook)
        self.notebook.add(status_tab, text="系统状态")
        
        # 数据库状态
        db_frame = ttk.LabelFrame(status_tab, text="数据库状态", padding="10")
        db_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.db_status_text = scrolledtext.ScrolledText(db_frame, width=70, height=15)
        self.db_status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(db_frame, text="刷新状态", command=self.refresh_db_status).grid(row=1, column=0, pady=10)
        
        # 配置权重
        status_tab.columnconfigure(0, weight=1)
        status_tab.rowconfigure(0, weight=1)
        db_frame.columnconfigure(0, weight=1)
        db_frame.rowconfigure(0, weight=1)
        
    def browse_file(self, file_var):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("CSV文件", "*.csv"), ("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
        )
        if filename:
            file_var.set(filename)
            
    def browse_export_path(self):
        """浏览导出路径"""
        filename = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if filename:
            self.export_path_var.set(filename)
            
    def hash_password(self, password):
        """哈希密码"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def log_message(self, message):
        """记录日志消息"""
        self.db_status_text.insert(tk.END, f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.db_status_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """清空日志"""
        self.db_status_text.delete(1.0, tk.END)
        
    def check_db_connection(self):
        """检查数据库连接"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查表是否存在
            tables = ['users', 'problems', 'contests', 'classes']
            for table in tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    self.log_message(f"✓ 表 '{table}' 存在")
                else:
                    self.log_message(f"✗ 表 '{table}' 不存在")
            
            conn.close()
            self.log_message("✓ 数据库连接成功")
            
        except Exception as e:
            self.log_message(f"✗ 数据库连接失败: {e}")
            
    def refresh_db_status(self):
        """刷新数据库状态"""
        self.clear_log()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取各表记录数
            tables = ['users', 'problems', 'contests', 'classes', 'submissions', 'class_enrollments']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                self.log_message(f"表 '{table}': {count} 条记录")
            
            # 获取用户角色分布
            cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
            roles = cursor.fetchall()
            for role, count in roles:
                self.log_message(f"  角色 '{role}': {count} 人")
            
            # 获取题目难度分布
            cursor.execute("SELECT difficulty, COUNT(*) FROM problems GROUP BY difficulty")
            difficulties = cursor.fetchall()
            for difficulty, count in difficulties:
                self.log_message(f"  难度 '{difficulty}': {count} 题")
            
            conn.close()
            self.log_message("✓ 数据库状态刷新完成")
            
        except Exception as e:
            self.log_message(f"✗ 刷新失败: {e}")
    
    def import_users(self):
        """导入用户"""
        file_path = self.user_file_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择用户文件")
            return
        
        try:
            if file_path.lower().endswith('.csv'):
                self._import_users_from_csv(file_path)
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                self._import_users_from_excel(file_path)
            else:
                messagebox.showerror("错误", "不支持的文件格式，请选择CSV或Excel文件")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入用户失败: {e}")
    
    def _import_users_from_csv(self, file_path):
        """从CSV导入用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        skipped = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = row.get('username', '').strip()
                    password = row.get('password', '123456').strip()
                    name = row.get('name', '').strip()
                    role = row.get('role', 'student').strip()
                    email = row.get('email', '').strip()
                    
                    if not username:
                        skipped += 1
                        continue
                    
                    # 检查用户是否已存在
                    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                    if cursor.fetchone():
                        skipped += 1
                        continue
                    
                    # 插入新用户
                    password_hash = self.hash_password(password)
                    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    cursor.execute('''
                        INSERT INTO users 
                        (username, password_hash, name, role, email, created_at, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (username, password_hash, name, role, email, created_at, True))
                    
                    imported += 1
                    self.log_message(f"导入用户: {username} ({name})")
            
            conn.commit()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个用户，跳过 {skipped} 个")
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _import_users_from_excel(self, file_path):
        """从Excel导入用户"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported = 0
            skipped = 0
            
            for _, row in df.iterrows():
                username = str(row.get('username', '')).strip()
                password = str(row.get('password', '123456')).strip()
                name = str(row.get('name', '')).strip()
                role = str(row.get('role', 'student')).strip()
                email = str(row.get('email', '')).strip()
                
                if not username:
                    skipped += 1
                    continue
                
                # 检查用户是否已存在
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    skipped += 1
                    continue
                
                # 插入新用户
                password_hash = self.hash_password(password)
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO users 
                    (username, password_hash, name, role, email, created_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (username, password_hash, name, role, email, created_at, True))
                
                imported += 1
                self.log_message(f"导入用户: {username} ({name})")
            
            conn.commit()
            conn.close()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个用户，跳过 {skipped} 个")
            
        except ImportError:
            messagebox.showerror("导入失败", "需要安装pandas库: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入用户失败: {e}")
    
    def import_problems(self):
        """导入题目"""
        file_path = self.problem_file_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择题目文件")
            return
        
        try:
            if file_path.lower().endswith('.csv'):
                self._import_problems_from_csv(file_path)
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                self._import_problems_from_excel(file_path)
            else:
                messagebox.showerror("错误", "不支持的文件格式，请选择CSV或Excel文件")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入题目失败: {e}")
    
    def _import_problems_from_csv(self, file_path):
        """从CSV导入题目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        skipped = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
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
                        skipped += 1
                        continue
                    
                    # 检查题目是否已存在
                    cursor.execute("SELECT id FROM problems WHERE title = ?", (title,))
                    if cursor.fetchone():
                        skipped += 1
                        continue
                    
                    # 插入新题目
                    created_by = 2  # test_teacher的用户ID
                    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    cursor.execute('''
                        INSERT INTO problems 
                        (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public))
                    
                    imported += 1
                    self.log_message(f"导入题目: {title} ({difficulty})")
            
            conn.commit()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个题目，跳过 {skipped} 个")
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _import_problems_from_excel(self, file_path):
        """从Excel导入题目"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported = 0
            skipped = 0
            
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
                    skipped += 1
                    continue
                
                # 检查题目是否已存在
                cursor.execute("SELECT id FROM problems WHERE title = ?", (title,))
                if cursor.fetchone():
                    skipped += 1
                    continue
                
                # 插入新题目
                created_by = 2  # test_teacher的用户ID
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO problems 
                    (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public))
                
                imported += 1
                self.log_message(f"导入题目: {title} ({difficulty})")
            
            conn.commit()
            conn.close()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个题目，跳过 {skipped} 个")
            
        except ImportError:
            messagebox.showerror("导入失败", "需要安装pandas库: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入题目失败: {e}")
    
    def import_classes(self):
        """导入班级"""
        file_path = self.class_file_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择班级文件")
            return
        
        try:
            if file_path.lower().endswith('.csv'):
                self._import_classes_from_csv(file_path)
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                self._import_classes_from_excel(file_path)
            else:
                messagebox.showerror("错误", "不支持的文件格式，请选择CSV或Excel文件")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入班级失败: {e}")
    
    def _import_classes_from_csv(self, file_path):
        """从CSV导入班级"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        skipped = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('name', '').strip()
                    description = row.get('description', '').strip()
                    teacher_id = int(row.get('teacher_id', 2))
                    
                    if not name:
                        skipped += 1
                        continue
                    
                    # 检查班级是否已存在
                    cursor.execute("SELECT id FROM classes WHERE name = ?", (name,))
                    if cursor.fetchone():
                        skipped += 1
                        continue
                    
                    # 插入新班级
                    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    cursor.execute('''
                        INSERT INTO classes 
                        (name, description, teacher_id, created_at)
                        VALUES (?, ?, ?, ?)
                    ''', (name, description, teacher_id, created_at))
                    
                    imported += 1
                    self.log_message(f"导入班级: {name}")
            
            conn.commit()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个班级，跳过 {skipped} 个")
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _import_classes_from_excel(self, file_path):
        """从Excel导入班级"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported = 0
            skipped = 0
            
            for _, row in df.iterrows():
                name = str(row.get('name', '')).strip()
                description = str(row.get('description', '')).strip()
                teacher_id = int(row.get('teacher_id', 2))
                
                if not name:
                    skipped += 1
                    continue
                
                # 检查班级是否已存在
                cursor.execute("SELECT id FROM classes WHERE name = ?", (name,))
                if cursor.fetchone():
                    skipped += 1
                    continue
                
                # 插入新班级
                created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT INTO classes 
                    (name, description, teacher_id, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (name, description, teacher_id, created_at))
                
                imported += 1
                self.log_message(f"导入班级: {name}")
            
            conn.commit()
            conn.close()
            messagebox.showinfo("导入完成", f"成功导入 {imported} 个班级，跳过 {skipped} 个")
            
        except ImportError:
            messagebox.showerror("导入失败", "需要安装pandas库: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("导入失败", f"导入班级失败: {e}")
    
    def manual_add_user(self):
        """手动添加用户"""
        username = self.manual_username.get().strip()
        password = self.manual_password.get().strip() or "123456"
        name = self.manual_name.get().strip()
        role = self.manual_role.get().strip() or "student"
        email = self.manual_email.get().strip()
        
        if not username:
            messagebox.showerror("错误", "用户名不能为空")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("错误", f"用户已存在: {username}")
                return
            
            # 插入新用户
            password_hash = self.hash_password(password)
            created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO users 
                (username, password_hash, name, role, email, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, name, role, email, created_at, True))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("成功", f"用户 {username} 添加成功")
            self.log_message(f"手动添加用户: {username} ({name})")
            
            # 清空表单
            self.manual_username.delete(0, tk.END)
            self.manual_name.delete(0, tk.END)
            self.manual_email.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("添加失败", f"添加用户失败: {e}")
    
    def manual_add_problem(self):
        """手动添加题目"""
        title = self.manual_title.get().strip()
        description = self.manual_description.get("1.0", tk.END).strip()
        difficulty = self.manual_difficulty.get().strip() or "easy"
        score = int(self.manual_score.get().strip() or "10")
        tags = self.manual_tags.get().strip()
        
        if not title:
            messagebox.showerror("错误", "题目标题不能为空")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查题目是否已存在
            cursor.execute("SELECT id FROM problems WHERE title = ?", (title,))
            if cursor.fetchone():
                messagebox.showerror("错误", f"题目已存在: {title}")
                return
            
            # 插入新题目
            created_by = 2  # test_teacher的用户ID
            created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            is_public = True
            
            cursor.execute('''
                INSERT INTO problems 
                (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, difficulty, score, 1000, 256, tags, created_by, created_at, is_public))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("成功", f"题目 '{title}' 添加成功")
            self.log_message(f"手动添加题目: {title} ({difficulty})")
            
            # 清空表单
            self.manual_title.delete(0, tk.END)
            self.manual_description.delete("1.0", tk.END)
            self.manual_tags.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("添加失败", f"添加题目失败: {e}")
    
    def export_to_json(self):
        """导出到JSON"""
        file_path = self.export_path_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择导出文件路径")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            data = {}
            
            # 导出用户
            if self.export_users_var.get():
                cursor.execute("SELECT * FROM users")
                users = [dict(row) for row in cursor.fetchall()]
                data['users'] = users
                self.log_message(f"导出 {len(users)} 个用户")
            
            # 导出题目
            if self.export_problems_var.get():
                cursor.execute("SELECT * FROM problems")
                problems = [dict(row) for row in cursor.fetchall()]
                data['problems'] = problems
                self.log_message(f"导出 {len(problems)} 个题目")
            
            # 导出比赛
            if self.export_contests_var.get():
                cursor.execute("SELECT * FROM contests")
                contests = [dict(row) for row in cursor.fetchall()]
                data['contests'] = contests
                self.log_message(f"导出 {len(contests)} 个比赛")
            
            # 导出班级
            if self.export_classes_var.get():
                cursor.execute("SELECT * FROM classes")
                classes = [dict(row) for row in cursor.fetchall()]
                data['classes'] = classes
                self.log_message(f"导出 {len(classes)} 个班级")
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            conn.close()
            messagebox.showinfo("导出成功", f"数据已导出到: {file_path}")
            self.log_message(f"✓ 数据导出完成: {file_path}")
            
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据失败: {e}")
            self.log_message(f"✗ 导出失败: {e}")
    
    def export_to_csv(self):
        """导出到CSV"""
        file_path = self.export_path_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择导出文件路径")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 导出用户
            if self.export_users_var.get():
                user_file = file_path.replace('.json', '_users.csv').replace('.csv', '_users.csv')
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                with open(user_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'username', 'password_hash', 'name', 'role', 'email', 'created_at', 'is_active'])
                    writer.writerows(users)
                self.log_message(f"导出用户到: {user_file}")
            
            # 导出题目
            if self.export_problems_var.get():
                problem_file = file_path.replace('.json', '_problems.csv').replace('.csv', '_problems.csv')
                cursor.execute("SELECT * FROM problems")
                problems = cursor.fetchall()
                with open(problem_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'title', 'description', 'difficulty', 'score', 'time_limit', 'memory_limit', 'tags', 'created_by', 'created_at', 'is_public'])
                    writer.writerows(problems)
                self.log_message(f"导出题目到: {problem_file}")
            
            # 导出比赛
            if self.export_contests_var.get():
                contest_file = file_path.replace('.json', '_contests.csv').replace('.csv', '_contests.csv')
                cursor.execute("SELECT * FROM contests")
                contests = cursor.fetchall()
                with open(contest_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'title', 'description', 'start_time', 'end_time', 'is_public', 'created_by', 'created_at'])
                    writer.writerows(contests)
                self.log_message(f"导出比赛到: {contest_file}")
            
            # 导出班级
            if self.export_classes_var.get():
                class_file = file_path.replace('.json', '_classes.csv').replace('.csv', '_classes.csv')
                cursor.execute("SELECT * FROM classes")
                classes = cursor.fetchall()
                with open(class_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'name', 'description', 'teacher_id', 'created_at'])
                    writer.writerows(classes)
                self.log_message(f"导出班级到: {class_file}")
            
            conn.close()
            messagebox.showinfo("导出成功", "数据已导出到CSV文件")
            self.log_message("✓ CSV导出完成")
            
        except Exception as e:
            messagebox.showerror("导出失败", f"导出CSV失败: {e}")
            self.log_message(f"✗ CSV导出失败: {e}")

def main():
    """主函数"""
    root = tk.Tk()
    app = DataImportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
