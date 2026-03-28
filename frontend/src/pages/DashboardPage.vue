<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <h1>CodeEdu 大厅</h1>
      <div>
        <button :class="['tab-button', activeTab === 'problems' ? 'active' : '']" @click="switchDashboardTab('problems')">公共题库</button>
        <button :class="['tab-button', activeTab === 'contests' ? 'active' : '']" @click="switchDashboardTab('contests')">比赛 / 测验</button>
        <button :class="['tab-button', activeTab === 'classes' ? 'active' : '']" @click="switchDashboardTab('classes')">班级管理</button>
      </div>
    </header>

    <main class="dashboard-main">
      <section v-if="activeTab === 'problems'" class="panel">
        <div class="panel-top">
          <h2>公共题库</h2>
          <div>
            <input type="text" v-model="search" @input="filterProblems" placeholder="搜索题号 / 标题 / 标签..." class="search-input" />
            <button class="btn btn-primary" @click="openImportModal('problem')">导入 / 发布题目</button>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card"><span>题库总量</span><strong>{{ filteredProblems.length }}</strong></div>
          <div class="stat-card"><span>简单题</span><strong>{{ problemStats.easy }}</strong></div>
          <div class="stat-card"><span>中等题</span><strong>{{ problemStats.medium }}</strong></div>
          <div class="stat-card"><span>困难题</span><strong>{{ problemStats.hard }}</strong></div>
        </div>

        <table class="table">
          <thead><tr><th>编号</th><th>标题</th><th>标签</th><th>难度</th><th>分值</th><th>操作</th></tr></thead>
          <tbody>
            <tr v-for="problem in filteredProblems" :key="problem.id">
              <td>{{ problem.id }}</td>
              <td>{{ problem.title }}</td>
              <td>{{ problem.tags.join(', ') }}</td>
              <td>{{ problem.level }}</td>
              <td>{{ problem.score }}</td>
              <td>
                <button class="btn btn-sm" @click="selectProblem(problem)">去工作区</button>
                <button class="btn btn-sm" @click="editProblem(problem)" style="margin-left:0.4rem;">编辑</button>
                <button class="btn btn-sm" @click="deleteProblemAction(problem)" style="margin-left:0.4rem;">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section v-if="activeTab === 'contests'" class="panel">
        <div class="panel-top">
          <h2>比赛 / 测验</h2>
          <div>
            <button class="btn btn-primary" @click="openContestBuilderModal">发布比赛 / 测验</button>
            <button class="btn" @click="openImportModal('contest')">导入比赛 JSON</button>
          </div>
        </div>
        <div class="item-grid">
          <div v-for="contest in contestList" :key="contest.id" class="item-card">
            <h3>{{ contest.title }}</h3>
            <p>{{ contest.description }}</p>
            <p>题目数：{{ contest.problemCount }} | 参与：{{ contest.participantCount }}</p>
            <button class="btn btn-sm" @click="openContest(contest)">进入</button>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'classes'" class="panel">
        <div class="panel-top">
          <h2>班级成绩管理</h2>
          <div>
            <button class="btn btn-primary" @click="openClassManagerModal">班级管理</button>
            <button class="btn" @click="openImportModal('student')">导入学生</button>
            <button class="btn" @click="exportClassGradesCSV">导出成绩单</button>
            <button class="btn" @click="generateClassReport">生成报告</button>
          </div>
        </div>

        <!-- 班级选择器 -->
        <div class="class-selector">
          <label>当前班级：</label>
          <select v-model="currentClassId" @change="switchClass" class="class-select">
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
          </select>
          <span class="class-info">{{ currentClassInfo }}</span>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <span>班级总人数</span>
            <strong>{{ classStats.totalStudents }} 人</strong>
            <small>较上周 +0%</small>
          </div>
          <div class="stat-card">
            <span>平均完成题数</span>
            <strong>{{ classStats.avgCompleted }} 题</strong>
            <small>班级排名: -</small>
          </div>
          <div class="stat-card">
            <span>活跃率 (有提交)</span>
            <strong>{{ classStats.activityRate }}%</strong>
            <small>参与度: {{ classStats.activityLevel }}</small>
          </div>
          <div class="stat-card">
            <span>平均分</span>
            <strong>{{ classStats.avgScore }}</strong>
            <small>最高分: {{ classStats.maxScore }}</small>
          </div>
        </div>

        <!-- 可视化图表区域 -->
        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <h3>成绩分布</h3>
              <button class="btn btn-sm" @click="refreshScoreChart">刷新</button>
            </div>
            <div class="chart-container" id="scoreDistributionChart">
              <div class="chart-placeholder">加载成绩分布图表...</div>
            </div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <h3>活跃度趋势</h3>
              <button class="btn btn-sm" @click="refreshActivityChart">刷新</button>
            </div>
            <div class="chart-container" id="activityTrendChart">
              <div class="chart-placeholder">加载活跃度趋势图表...</div>
            </div>
          </div>
        </div>

        <!-- 学生列表 -->
        <div class="student-list-container">
          <div class="list-header">
            <div>
              <h3>学生列表</h3>
              <p>支持点击查看详情、批量操作</p>
            </div>
            <div class="list-actions">
              <button class="btn btn-sm" @click="selectAllStudents">全选</button>
              <button class="btn btn-sm" @click="clearStudentSelection">取消选择</button>
              <button class="btn btn-sm btn-danger" @click="batchRemoveStudents">批量移除</button>
            </div>
          </div>
          
          <table class="table">
            <thead>
              <tr>
                <th><input type="checkbox" v-model="selectAll" @change="toggleAllStudents"></th>
                <th>学号</th>
                <th>姓名</th>
                <th>总分</th>
                <th>AC 题数</th>
                <th>提交次数</th>
                <th>最近提交</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in paginatedStudents" :key="student.id">
                <td><input type="checkbox" v-model="selectedStudents" :value="student.id"></td>
                <td>{{ student.id }}</td>
                <td>
                  <div class="student-avatar">{{ student.name.charAt(0) }}</div>
                  {{ student.name }}
                </td>
                <td class="score-cell" :class="getScoreClass(student.score)">{{ student.score || 0 }}</td>
                <td>{{ student.solvedCount || 0 }}</td>
                <td>{{ student.submissionCount || 0 }}</td>
                <td>{{ formatDate(student.lastSubmit) }}</td>
                <td>
                  <button class="btn btn-sm" @click="viewStudentDetails(student)">详情</button>
                  <button class="btn btn-sm btn-danger" @click="removeStudent(student)">移除</button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div class="pagination">
            <div>已选择 {{ selectedStudents.length }} 名学生</div>
            <div class="pagination-controls">
              <button class="btn btn-sm" @click="previousPage" :disabled="currentPage === 1">上一页</button>
              <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
              <button class="btn btn-sm" @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="dashboard-footer">CodeEdu 前端原型：迁移于 111.html</footer>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Problem } from '@/api'
import { useProblemStore } from '@/stores/problem'
import { useContestStore } from '@/stores/contest'
import { useClassStore } from '@/stores/class'
import { useUserStore } from '@/stores/user'
import { createProblem, deleteProblem, updateProblem, createContest, addStudent } from '@/api'

const router = useRouter()
const problemStore = useProblemStore()
const contestStore = useContestStore()
const classStore = useClassStore()
const userStore = useUserStore()

const activeTab = ref<'problems' | 'contests' | 'classes'>('problems')
const search = ref('')

// 班级管理相关状态
const currentClassId = ref('default')
const classes = ref([
  { id: 'default', name: '默认班级', description: '系统默认班级' }
])
const selectedStudents = ref<string[]>([])
const selectAll = ref(false)
const currentPage = ref(1)
const studentsPerPage = 10

// 模拟学生数据
const mockStudents = ref([
  { id: 'S001', name: '张三', score: 85, solvedCount: 5, submissionCount: 12, lastSubmit: '2024-01-15T10:30:00' },
  { id: 'S002', name: '李四', score: 92, solvedCount: 7, submissionCount: 15, lastSubmit: '2024-01-14T14:20:00' },
  { id: 'S003', name: '王五', score: 78, solvedCount: 4, submissionCount: 10, lastSubmit: '2024-01-13T09:15:00' },
  { id: 'S004', name: '赵六', score: 65, solvedCount: 3, submissionCount: 8, lastSubmit: '2024-01-12T16:45:00' },
  { id: 'S005', name: '钱七', score: 88, solvedCount: 6, submissionCount: 14, lastSubmit: '2024-01-11T11:10:00' },
  { id: 'S006', name: '孙八', score: 95, solvedCount: 8, submissionCount: 18, lastSubmit: '2024-01-10T13:25:00' },
  { id: 'S007', name: '周九', score: 72, solvedCount: 4, submissionCount: 9, lastSubmit: '2024-01-09T15:40:00' },
  { id: 'S008', name: '吴十', score: 81, solvedCount: 5, submissionCount: 11, lastSubmit: '2024-01-08T10:05:00' },
  { id: 'S009', name: '郑十一', score: 90, solvedCount: 7, submissionCount: 16, lastSubmit: '2024-01-07T14:50:00' },
  { id: 'S010', name: '王十二', score: 76, solvedCount: 4, submissionCount: 10, lastSubmit: '2024-01-06T09:30:00' },
  { id: 'S011', name: '李十三', score: 83, solvedCount: 5, submissionCount: 12, lastSubmit: '2024-01-05T11:20:00' },
  { id: 'S012', name: '张十四', score: 79, solvedCount: 4, submissionCount: 11, lastSubmit: '2024-01-04T16:15:00' }
])

const problemStats = computed(() => problemStore.stats)
const filteredProblems = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return problemStore.problems
  return problemStore.problems.filter((p) =>
    p.id.includes(q) || p.title.toLowerCase().includes(q) || p.tags.join(' ').toLowerCase().includes(q),
  )
})

const contestList = computed(() => {
  return contestStore.contests.map(c => ({
    ...c,
    problemCount: 5, // 模拟数据
    participantCount: Math.floor(Math.random() * 50) + 10 // 模拟数据
  }))
})

// 移除重复的 classStats 定义，使用下面的增强版

watch(activeTab, (tab) => {
  if (tab === 'problems') {
    problemStore.loadProblems()
  } else if (tab === 'contests') {
    contestStore.loadContests()
  } else if (tab === 'classes') {
    classStore.loadStudents()
  }
})

onMounted(async () => {
  await problemStore.loadProblems()
  await contestStore.loadContests()
  await classStore.loadStudents()
})

const switchDashboardTab = (tab: 'problems' | 'contests' | 'classes') => {
  activeTab.value = tab
}

const openImportModal = async (type: 'problem' | 'contest' | 'student') => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可操作')
    return
  }

  if (type === 'problem') {
    const title = window.prompt('新题标题', '新题') || '新题'
    const newProblem = {
      title,
      tags: ['新增'],
      level: '简单',
      score: 10,
      description: '这是一道新题',
      testcase: '',
      example: '',
    }
    await createProblem(newProblem)
    await problemStore.loadProblems()
    return
  }

  if (type === 'contest') {
    const title = window.prompt('比赛名称', '新比赛') || '新比赛'
    const contest = await createContest({ title, description: '自动创建', problemCount: problemStore.problems.length })
    contestStore.contests.push(contest)
    return
  }

  if (type === 'student') {
    const id = window.prompt('学号', `S${Date.now()}`) || `S${Date.now()}`
    const name = window.prompt('姓名', '新学生') || '新学生'
    const student = { id, name, score: 0, solvedCount: 0, lastSubmit: new Date().toLocaleString() }
    await addStudent(student)
    await classStore.loadStudents()
    return
  }
}

const openContestBuilderModal = async () => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可以发布比赛/测验')
    return
  }
  const title = window.prompt('比赛名称', '新比赛') || '新比赛'
  const description = window.prompt('比赛描述', '自动创建') || '自动创建'
  await createContest({ title, description, problemCount: problemStore.problems.length })
  await contestStore.loadContests()
}

const exportClassGradesCSV = () => {
  const csv = ['学号,姓名,总分,AC题数,最近提交', ...classStore.students.map((s) => `${s.id},${s.name},${s.score},${s.solvedCount},${s.lastSubmit}`)].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'class_grades.csv'
  link.click()
  URL.revokeObjectURL(url)
}

const selectProblem = (problem: any) => {
  problemStore.select(problem.id)
  router.push({ name: 'workspace', query: { problemId: problem.id } })
}

const openContest = (contest: any) => {
  window.alert(`进入比赛：${contest.title}`)
}

const deleteProblemAction = async (problem: Problem) => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可删除题目')
    return
  }
  if (!window.confirm(`确认删除题目 ${problem.title}？`)) {
    return
  }
  await deleteProblem(problem.id)
  await problemStore.loadProblems()
}

const editProblem = async (problem: Problem) => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可编辑题目')
    return
  }
  const title = window.prompt('题目名称', problem.title)
  if (!title) return
  const newProblem = {
    title,
    tags: problem.tags,
    level: problem.level,
    score: problem.score,
    description: problem.description,
    testcase: problem.testcase,
    example: problem.example,
  }
  await updateProblem(problem.id, newProblem)
  await problemStore.loadProblems()
}

const importStudents = () => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可导入学生')
    return
  }
  const sample = classStore.students.map((s) => ({ ...s }))
  classStore.importStudents(sample)
}

// 班级管理计算属性
const currentClassInfo = computed(() => {
  const cls = classes.value.find(c => c.id === currentClassId.value)
  return cls ? `${cls.name} - ${mockStudents.value.length} 名学生` : '未知班级'
})

const classStats = computed(() => {
  const students = mockStudents.value
  const total = students.length
  const totalScore = students.reduce((sum, s) => sum + (s.score || 0), 0)
  const totalSolved = students.reduce((sum, s) => sum + (s.solvedCount || 0), 0)
  const activeStudents = students.filter(s => (s.solvedCount || 0) > 0).length
  const maxScore = Math.max(...students.map(s => s.score || 0))
  
  return {
    totalStudents: total,
    avgCompleted: total === 0 ? '0.0' : (totalSolved / total).toFixed(1),
    activityRate: total === 0 ? '0' : Math.round((activeStudents / total) * 100),
    activityLevel: activeStudents === 0 ? '低' : activeStudents < total / 2 ? '中' : '高',
    avgScore: total === 0 ? 0 : Math.round(totalScore / total),
    maxScore: maxScore
  }
})

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * studentsPerPage
  const end = start + studentsPerPage
  return mockStudents.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(mockStudents.value.length / studentsPerPage)
})

// 班级管理方法
const switchClass = () => {
  // 切换班级逻辑
  console.log('切换到班级:', currentClassId.value)
  currentPage.value = 1
  selectedStudents.value = []
}

const openClassManagerModal = () => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可管理班级')
    return
  }
  window.alert('班级管理功能开发中...')
}

const generateClassReport = () => {
  if (userStore.role !== 'teacher') {
    window.alert('仅教师可生成报告')
    return
  }
  window.alert('班级报告生成功能开发中...')
}

const toggleAllStudents = () => {
  if (selectAll.value) {
    selectedStudents.value = paginatedStudents.value.map(s => s.id)
  } else {
    selectedStudents.value = []
  }
}

const selectAllStudents = () => {
  selectedStudents.value = paginatedStudents.value.map(s => s.id)
  selectAll.value = true
}

const clearStudentSelection = () => {
  selectedStudents.value = []
  selectAll.value = false
}

const batchRemoveStudents = () => {
  if (selectedStudents.value.length === 0) {
    window.alert('请先选择要移除的学生')
    return
  }
  
  if (window.confirm(`确定要移除选中的 ${selectedStudents.value.length} 名学生吗？`)) {
    mockStudents.value = mockStudents.value.filter(s => !selectedStudents.value.includes(s.id))
    selectedStudents.value = []
    selectAll.value = false
    window.alert('已移除选中的学生')
  }
}

const removeStudent = (student: any) => {
  if (window.confirm(`确定要移除学生 ${student.name} 吗？`)) {
    mockStudents.value = mockStudents.value.filter(s => s.id !== student.id)
    window.alert('已移除学生')
  }
}

const viewStudentDetails = (student: any) => {
  window.alert(`学生详情：
学号: ${student.id}
姓名: ${student.name}
总分: ${student.score}
AC题数: ${student.solvedCount}
提交次数: ${student.submissionCount}
最近提交: ${formatDate(student.lastSubmit)}`)
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const refreshScoreChart = () => {
  // 模拟刷新图表
  console.log('刷新成绩分布图表')
}

const refreshActivityChart = () => {
  // 模拟刷新图表
  console.log('刷新活跃度趋势图表')
}

const getScoreClass = (score: number) => {
  if (score >= 90) return 'score-high'
  if (score >= 80) return 'score-medium'
  if (score >= 60) return 'score-low'
  return 'score-fail'
}

const formatDate = (dateString: string) => {
  if (!dateString) return '--'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN')
  } catch {
    return dateString
  }
}

// 监听选中学生变化
watch(selectedStudents, (newVal) => {
  const currentPageStudents = paginatedStudents.value.map(s => s.id)
  selectAll.value = newVal.length > 0 && currentPageStudents.every(id => newVal.includes(id))
})
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
}

.tab-button {
  margin-left: 0.5rem;
  padding: 0.55rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  background: #f8fafc;
  color: #334155;
  font-weight: 500;
  cursor: pointer;
}

.tab-button.active,
.tab-button:hover {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}

.dashboard-main {
  padding: 1.2rem 1.5rem;
  background: #f8fafc;
}

.panel {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem;
}

.panel-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 0.75rem;
  margin: 0 0 1rem;
}

.stat-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.6rem;
  padding: 0.75rem;
  background: #f8fafc;
}

.stat-card span {
  font-size: 0.75rem;
  color: #64748b;
}

.stat-card strong {
  display: block;
  font-size: 1.2rem;
  margin-top: 0.25rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #e2e8f0;
  padding: 0.65rem 0.75rem;
  text-align: left;
}

.table th {
  background: #f1f5f9;
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.9rem;
}

.item-card {
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.65rem;
  background: #fff;
}

.btn {
  border: 1px solid #cbd5e1;
  background: #fff;
  color: #334155;
  padding: 0.5rem 0.8rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-left: 0.5rem;
}

.btn-primary {
  border-color: #3b82f6;
  background: #3b82f6;
  color: #fff;
}

.btn-sm {
  padding: 0.35rem 0.7rem;
  font-size: 0.82rem;
}

.search-input {
  padding: 0.45rem 0.7rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  width: 220px;
}

.dashboard-footer {
  text-align: center;
  margin: 1.2rem 0 0;
  color: #94a3b8;
}

/* 班级管理样式 */
.class-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.class-select {
  padding: 0.5rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  background: white;
  color: #334155;
  font-weight: 500;
}

.class-info {
  margin-left: auto;
  color: #64748b;
  font-size: 0.9rem;
}

.stat-card small {
  display: block;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.chart-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem;
  background: white;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #334155;
}

.chart-container {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px dashed #cbd5e1;
}

.chart-placeholder {
  color: #94a3b8;
  font-size: 0.9rem;
}

.student-list-container {
  margin-top: 1.5rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.list-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #334155;
}

.list-header p {
  margin: 0.25rem 0 0;
  color: #64748b;
  font-size: 0.85rem;
}

.list-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-danger {
  border-color: #ef4444;
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
  border-color: #dc2626;
}

.student-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  margin-right: 0.5rem;
}

.score-cell {
  font-weight: bold;
}

.score-high {
  color: #10b981;
}

.score-medium {
  color: #f59e0b;
}

.score-low {
  color: #f97316;
}

.score-fail {
  color: #ef4444;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  color: #64748b;
  font-size: 0.9rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
