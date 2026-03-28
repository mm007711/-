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
            <button class="btn btn-primary" @click="importStudents">导入学生名单</button>
            <button class="btn" @click="exportClassGradesCSV">导出成绩单</button>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card"><span>班级人数</span><strong>{{ classStats.students }}</strong></div>
          <div class="stat-card"><span>平均完成</span><strong>{{ classStats.avgCompleted }}</strong></div>
          <div class="stat-card"><span>活跃率</span><strong>{{ classStats.activity }}</strong></div>
        </div>

        <div class="table-container">
          <table class="table">
            <thead><tr><th>学号</th><th>姓名</th><th>总分</th><th>AC 题数</th><th>最近提交</th></tr></thead>
            <tbody>
              <tr v-for="student in classStore.students" :key="student.id">
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.score }}</td>
                <td>{{ student.solvedCount }}</td>
                <td>{{ student.lastSubmit }}</td>
              </tr>
            </tbody>
          </table>
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

const problemStats = computed(() => problemStore.stats)
const filteredProblems = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return problemStore.problems
  return problemStore.problems.filter((p) =>
    p.id.includes(q) || p.title.toLowerCase().includes(q) || p.tags.join(' ').toLowerCase().includes(q),
  )
})

const classStats = computed(() => classStore.stats)

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

import { createProblem, deleteProblem, updateProblem, createContest, addStudent } from '@/api'

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
</style>
