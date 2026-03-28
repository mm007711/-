export type Problem = {
  id: number
  title: string
  description: string
  difficulty: string
  score: number
  time_limit: number
  memory_limit: number
  tags: string
  is_public: boolean
  created_by?: number
  created_at: string
}

export type Contest = {
  id: number
  title: string
  description: string
  start_time: string
  end_time: string
  is_public: boolean
  created_by?: number
  created_at: string
}

export type User = {
  id: number
  username: string
  name: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

export type Submission = {
  id: number
  user_id: number
  problem_id: number
  contest_id?: number
  code: string
  language: string
  status: string
  score: number
  time_used?: number
  memory_used?: number
  submitted_at: string
  judged_at?: string
}

export type JudgeCase = {
  caseId: number
  input: string
  expected: string
  actual: string
  status: string
  runtimeMs: number
}

export type JudgeResult = {
  status: string
  report: string
  score: number
  total_cases: number
  passed_cases: number
  cases: JudgeCase[]
}

export type Class = {
  id: number
  name: string
  description?: string
  teacher_id: number
  created_at: string
}

export type ClassEnrollment = {
  id: number
  class_id: number
  student_id: number
  score: number
  solved_count: number
  enrolled_at: string
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

function getToken() {
  return localStorage.getItem('codeedu_token') || ''
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }
  const token = getToken()
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const errorText = await res.text()
    throw new Error(`API Error ${res.status}: ${errorText}`)
  }
  return (await res.json()) as T
}

// 认证相关
export const login = async (username: string, password: string) => {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

  if (!res.ok) {
    throw new Error('登录失败：用户名或密码错误')
  }

  const data = await res.json()
  localStorage.setItem('codeedu_token', data.access_token)
  return data
}

export const me = async (): Promise<User> => {
  return request<User>('/api/auth/me')
}

export const register = async (username: string, password: string): Promise<User> => {
  return request<User>('/api/users/', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
}

// 题目管理
export const fetchProblems = async (): Promise<Problem[]> => {
  return request<Problem[]>('/api/problems')
}

export const getProblem = async (problemId: number): Promise<Problem> => {
  return request<Problem>(`/api/problems/${problemId}`)
}

export const createProblem = async (problem: Omit<Problem, 'id' | 'created_by' | 'created_at'>): Promise<Problem> => {
  return request<Problem>('/api/problems', { 
    method: 'POST', 
    body: JSON.stringify(problem) 
  })
}

export const updateProblem = async (problemId: number, problem: Omit<Problem, 'id' | 'created_by' | 'created_at'>): Promise<Problem> => {
  return request<Problem>(`/api/problems/${problemId}`, { 
    method: 'PUT', 
    body: JSON.stringify(problem) 
  })
}

export const deleteProblem = async (problemId: number): Promise<void> => {
  await request<void>(`/api/problems/${problemId}`, { method: 'DELETE' })
}

// 比赛管理
export const fetchContests = async (): Promise<Contest[]> => {
  return request<Contest[]>('/api/contests')
}

export const createContest = async (contest: Omit<Contest, 'id' | 'created_by' | 'created_at'>): Promise<Contest> => {
  return request<Contest>('/api/contests', { 
    method: 'POST', 
    body: JSON.stringify(contest) 
  })
}

// 提交管理
export const createSubmission = async (
  problemId: number, 
  code: string, 
  language: string,
  contestId?: number
): Promise<Submission> => {
  return request<Submission>('/api/submissions', {
    method: 'POST',
    body: JSON.stringify({
      problem_id: problemId,
      code,
      language,
      contest_id: contestId
    })
  })
}

export const getSubmission = async (submissionId: number): Promise<Submission> => {
  return request<Submission>(`/api/submissions/${submissionId}`)
}

export const getUserSubmissions = async (userId: number): Promise<Submission[]> => {
  return request<Submission[]>(`/api/submissions/user/${userId}`)
}

// 班级管理
export const fetchClasses = async (): Promise<Class[]> => {
  return request<Class[]>('/api/classes')
}

export const createClass = async (classData: Omit<Class, 'id' | 'teacher_id' | 'created_at'>): Promise<Class> => {
  return request<Class>('/api/classes', {
    method: 'POST',
    body: JSON.stringify(classData)
  })
}

export const enrollStudent = async (classId: number, studentId: number): Promise<ClassEnrollment> => {
  return request<ClassEnrollment>(`/api/classes/${classId}/enroll`, {
    method: 'POST',
    body: JSON.stringify({
      student_id: studentId,
      score: 0,
      solved_count: 0
    })
  })
}

// 评测相关（兼容旧API）
export const runJudge = async (code: string, problemId: string): Promise<JudgeResult> => {
  return request<JudgeResult>(`/api/judge/run?problem_id=${encodeURIComponent(problemId)}`, {
    method: 'POST',
    body: JSON.stringify({ code }),
  })
}

// 工具函数
export const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

export const getDifficultyColor = (difficulty: string): string => {
  switch (difficulty.toLowerCase()) {
    case 'easy':
    case '简单':
      return 'green'
    case 'medium':
    case '中等':
      return 'orange'
    case 'hard':
    case '困难':
      return 'red'
    default:
      return 'gray'
  }
}
