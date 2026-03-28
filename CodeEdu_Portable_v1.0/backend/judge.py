import subprocess
import tempfile
import os
import time
import resource
import signal
from typing import Dict, List, Tuple, Optional
from models import Problem, TestCase

class JudgeResult:
    def __init__(self):
        self.status = "pending"
        self.score = 0
        self.time_used = 0
        self.memory_used = 0
        self.cases = []

class CodeExecutor:
    def __init__(self, language: str, code: str, problem: Problem):
        self.language = language
        self.code = code
        self.problem = problem
        self.time_limit = problem.time_limit / 1000  # 转换为秒
        self.memory_limit = problem.memory_limit * 1024  # 转换为KB
        
    def create_temp_file(self) -> str:
        """创建临时文件并写入代码"""
        suffix = {
            "python": ".py",
            "javascript": ".js",
            "cpp": ".cpp",
            "c": ".c",
            "java": ".java"
        }.get(self.language, ".txt")
        
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(self.code)
        return path
    
    def run_python(self, input_data: str) -> Tuple[str, float, int]:
        """运行Python代码"""
        code_path = self.create_temp_file()
        try:
            # 准备输入
            start_time = time.time()
            
            # 使用subprocess运行代码
            process = subprocess.Popen(
                ['python', code_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=self.set_limits
            )
            
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=self.time_limit)
                elapsed = time.time() - start_time
                
                if process.returncode != 0:
                    return f"Runtime Error: {stderr}", elapsed, 0
                    
                return stdout.strip(), elapsed, 0  # 内存使用暂时返回0
                
            except subprocess.TimeoutExpired:
                process.kill()
                return "Time Limit Exceeded", self.time_limit, 0
                
        except Exception as e:
            return f"System Error: {str(e)}", 0, 0
        finally:
            os.unlink(code_path)
    
    def run_javascript(self, input_data: str) -> Tuple[str, float, int]:
        """运行JavaScript代码"""
        code_path = self.create_temp_file()
        try:
            start_time = time.time()
            
            process = subprocess.Popen(
                ['node', code_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=self.set_limits
            )
            
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=self.time_limit)
                elapsed = time.time() - start_time
                
                if process.returncode != 0:
                    return f"Runtime Error: {stderr}", elapsed, 0
                    
                return stdout.strip(), elapsed, 0
                
            except subprocess.TimeoutExpired:
                process.kill()
                return "Time Limit Exceeded", self.time_limit, 0
                
        except Exception as e:
            return f"System Error: {str(e)}", 0, 0
        finally:
            os.unlink(code_path)
    
    def run_cpp(self, input_data: str) -> Tuple[str, float, int]:
        """运行C++代码"""
        code_path = self.create_temp_file()
        exe_path = code_path + ".exe"
        
        try:
            # 编译
            compile_process = subprocess.Popen(
                ['g++', code_path, '-o', exe_path, '-std=c++11'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            compile_stdout, compile_stderr = compile_process.communicate(timeout=10)
            
            if compile_process.returncode != 0:
                return f"Compilation Error: {compile_stderr}", 0, 0
            
            # 运行
            start_time = time.time()
            run_process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=self.set_limits
            )
            
            try:
                stdout, stderr = run_process.communicate(input=input_data, timeout=self.time_limit)
                elapsed = time.time() - start_time
                
                if run_process.returncode != 0:
                    return f"Runtime Error: {stderr}", elapsed, 0
                    
                return stdout.strip(), elapsed, 0
                
            except subprocess.TimeoutExpired:
                run_process.kill()
                return "Time Limit Exceeded", self.time_limit, 0
                
        except Exception as e:
            return f"System Error: {str(e)}", 0, 0
        finally:
            if os.path.exists(code_path):
                os.unlink(code_path)
            if os.path.exists(exe_path):
                os.unlink(exe_path)
    
    def set_limits(self):
        """设置资源限制"""
        if hasattr(resource, 'RLIMIT_CPU'):
            resource.setrlimit(resource.RLIMIT_CPU, (self.time_limit, self.time_limit + 1))
        if hasattr(resource, 'RLIMIT_AS'):
            resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
    
    def execute(self, input_data: str) -> Tuple[str, float, int]:
        """执行代码并返回结果"""
        if self.language == "python":
            return self.run_python(input_data)
        elif self.language == "javascript":
            return self.run_javascript(input_data)
        elif self.language == "cpp":
            return self.run_cpp(input_data)
        else:
            return f"Unsupported language: {self.language}", 0, 0

class Judge:
    def __init__(self, problem: Problem, code: str, language: str):
        self.problem = problem
        self.code = code
        self.language = language
        self.executor = CodeExecutor(language, code, problem)
        self.result = JudgeResult()
    
    def compare_output(self, expected: str, actual: str) -> bool:
        """比较输出是否相等（简单实现）"""
        # 去除首尾空白字符后比较
        return expected.strip() == actual.strip()
    
    def judge_test_case(self, test_case: TestCase) -> Dict:
        """评测单个测试用例"""
        try:
            output, time_used, memory_used = self.executor.execute(test_case.input_data)
            
            case_result = {
                "test_case_id": test_case.id,
                "input": test_case.input_data[:100] + ("..." if len(test_case.input_data) > 100 else ""),
                "expected": test_case.expected_output[:100] + ("..." if len(test_case.expected_output) > 100 else ""),
                "actual": output[:100] + ("..." if len(output) > 100 else ""),
                "time_used": round(time_used * 1000, 2),  # 转换为毫秒
                "memory_used": memory_used,
            }
            
            if "Time Limit Exceeded" in output:
                case_result["status"] = "time_limit_exceeded"
            elif "Runtime Error" in output:
                case_result["status"] = "runtime_error"
            elif "Compilation Error" in output:
                case_result["status"] = "compilation_error"
            elif "System Error" in output:
                case_result["status"] = "system_error"
            elif self.compare_output(test_case.expected_output, output):
                case_result["status"] = "accepted"
            else:
                case_result["status"] = "wrong_answer"
                
            return case_result
            
        except Exception as e:
            return {
                "test_case_id": test_case.id,
                "input": test_case.input_data[:100],
                "expected": test_case.expected_output[:100],
                "actual": f"Judge Error: {str(e)}",
                "status": "judge_error",
                "time_used": 0,
                "memory_used": 0,
            }
    
    def judge(self, test_cases: List[TestCase]) -> JudgeResult:
        """评测所有测试用例"""
        self.result.cases = []
        passed = 0
        
        for test_case in test_cases:
            case_result = self.judge_test_case(test_case)
            self.result.cases.append(case_result)
            
            if case_result["status"] == "accepted":
                passed += 1
        
        # 计算总分
        total_cases = len(test_cases)
        if total_cases > 0:
            self.result.score = int((passed / total_cases) * self.problem.score)
        
        # 确定最终状态
        if passed == total_cases:
            self.result.status = "accepted"
        elif any(case["status"] == "time_limit_exceeded" for case in self.result.cases):
            self.result.status = "time_limit_exceeded"
        elif any(case["status"] == "runtime_error" for case in self.result.cases):
            self.result.status = "runtime_error"
        elif any(case["status"] == "compilation_error" for case in self.result.cases):
            self.result.status = "compilation_error"
        else:
            self.result.status = "wrong_answer"
        
        # 计算总时间和内存使用
        self.result.time_used = sum(case["time_used"] for case in self.result.cases)
        self.result.memory_used = max((case["memory_used"] for case in self.result.cases), default=0)
        
        return self.result

# 简单的评测函数（用于测试）
def simple_judge(code: str, language: str, problem: Problem, test_cases: List[TestCase]) -> Dict:
    """简单的评测函数，返回评测结果"""
    judge = Judge(problem, code, language)
    result = judge.judge(test_cases)
    
    return {
        "status": result.status,
        "score": result.score,
        "time_used": result.time_used,
        "memory_used": result.memory_used,
        "cases": result.cases,
        "report": f"通过 {len([c for c in result.cases if c['status'] == 'accepted'])}/{len(result.cases)} 个测试用例"
    }
