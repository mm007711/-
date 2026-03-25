<template>
  <div class="workspace-page">
    <div class="workspace-header">
      <div class="workspace-top-left">
        <button @click="goBack" class="back-btn">返回大厅</button>
        <select class="problem-select" v-model="currentProblemId" @change="switchProblem(currentProblemId)">
          <option v-for="p in problemList" :key="p.id" :value="p.id">{{ p.id }} - {{ p.title }}</option>
        </select>
        <button class="btn btn-sm" @click="openProblemListModal">题目列表</button>
      </div>
      <div class="workspace-top-right">
        <select v-model="language" class="language-select" @change="resetCode()">
          <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
        </select>
        <button class="btn btn-sm" @click="fillDemoAnswer">✨ 演示代码</button>
        <button class="btn btn-sm" @click="resetCode">↺ 重置代码</button>
      </div>
    </div>

    <div class="workspace-container">
      <section class="left-panel">
        <div class="problem-info">
          <h2>题目详情</h2>
          <p><strong>描述：</strong>{{ currentProblem.description }}</p>
          <p><strong>难度：</strong>{{ currentProblem.level }} | <strong>分值：</strong>{{ currentProblem.score }}</p>
          <p><strong>示例：</strong></p>
          <pre class="example">{{ currentProblem.example }}</pre>
        </div>
      </section>

      <div class="resizer"></div>

      <section class="right-panel">
        <div class="editor-section">
          <h3>代码编辑器</h3>
          <textarea
            v-model="code"
            placeholder="在这里编写您的代码..."
            class="code-editor"
          ></textarea>
        </div>

        <div class="console-section">
          <div class="tabs">
            <button
              v-for="tab in consoleTabs"
              :key="tab"
              @click="activeTab = tab"
              :class="['tab-button', { active: activeTab === tab }]"
            >
              {{ tab }}
            </button>
          </div>
          <div class="tab-content">
            <div v-if="activeTab === '测试用例'" class="tab-pane">
              <p>当前测试输入：{{ currentProblem.testcase }}</p>
            </div>
            <div v-if="activeTab === '判题结果'" class="tab-pane">
              <p>{{ judgeResult }}</p>
              <table class="table" style="margin-top: 0.6rem;">
                <thead><tr><th>用例</th><th>输入</th><th>预期</th><th>实际</th><th>状态</th><th>耗时(ms)</th></tr></thead>
                <tbody>
                  <tr v-for="caseItem in judgeCases" :key="caseItem.caseId">
                    <td>{{ caseItem.caseId }}</td>
                    <td>{{ caseItem.input }}</td>
                    <td>{{ caseItem.expected }}</td>
                    <td>{{ caseItem.actual }}</td>
                    <td>{{ caseItem.status }}</td>
                    <td>{{ caseItem.runtimeMs }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="activeTab === '运行日志'" class="tab-pane">
              <pre>{{ runLog }}</pre>
            </div>
            <div v-if="activeTab === '提交历史'" class="tab-pane">
              <ul>
                <li v-for="item in submitHistory" :key="item.time">{{ item.time }} - {{ item.status }}</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="runCode" class="btn btn-run">运行测试</button>
          <button @click="submitCode" class="btn btn-submit">正式提交</button>
        </div>
      </section>
    </div>

    <div v-if="isProblemListModalOpen" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>题目列表</h3>
          <button class="text-slate-500 hover:text-slate-900" @click="closeProblemListModal">✕</button>
        </div>
        <div class="modal-body">
          <ul>
            <li v-for="p in problemList" :key="p.id" class="modal-item">
              <button class="block w-full text-left" @click="switchProblem(p.id)">{{ p.id }} - {{ p.title }}</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useProblemStore } from '@/stores/problem'
import { useUserStore } from '@/stores/user'
import { runJudge, type JudgeCase } from '@/api'

const router = useRouter()
const route = useRoute()
const problemStore = useProblemStore()
const userStore = useUserStore()

const code = ref('')
const activeTab = ref('测试用例')
const consoleTabs = ['测试用例', '判题结果', '运行日志', '提交历史']
const judgeResult = ref('尚未运行')
const judgeCases = ref<JudgeCase[]>([])
const runLog = ref('')
const language = ref('JavaScript')
const languages = ['JavaScript', 'Python', 'C++']

const submitHistory = reactive([{
  time: '2026-03-25 10:32',
  status: 'AC',
}, {
  time: '2026-03-25 10:28',
  status: 'WA',
}])

const currentProblem = reactive({
  title: '加载中',
  description: '',
  level: '简单',
  score: 0,
  testcase: '',
  example: '',
})

const currentProblemId = ref((route.query.problemId as string) || '101')
const problemList = computed(() => problemStore.problems)

watch(route, (newRoute) => {
  currentProblemId.value = (newRoute.query.problemId as string) || '101'
})

const getDefaultCodeTemplate = () => {
  switch (language.value) {
    case 'Python':
      return `def solution(nums, target):\n    # TODO: 实现两数之和\n    return []`
    case 'C++':
      return `#include <vector>\nusing namespace std;\nvector<int> solution(vector<int>& nums, int target) {\n    // TODO\n    return {};\n}`
    default:
      return `function solution(nums, target) {\n  // TODO\n  return []\n}`
  }
}

const loadProblemFromRoute = () => {
  const selectedId = currentProblemId.value
  problemStore.selectedProblemId.value = selectedId
  const p = problemStore.current
  if (p) {
    Object.assign(currentProblem, p)
    const saved = localStorage.getItem(`code_${selectedId}_${language.value}`)
    code.value = saved ?? getDefaultCodeTemplate()
  }
}

watch([() => route.query.problemId, language], () => {
  loadProblemFromRoute()
})

watch(code, (newCode) => {
  localStorage.setItem(`code_${currentProblemId.value}_${language.value}`, newCode)
})

onMounted(async () => {
  if (problemStore.problems.length === 0) {
    await problemStore.loadProblems()
  }
  loadProblemFromRoute()
})

const goBack = () => {
  router.push({ name: 'dashboard' })
}

const runCode = async () => {
  runLog.value = `执行代码:\n${code.value}\n\n测试输入：${currentProblem.testcase}`
  const judge = await runJudge(code.value, currentProblemId.value)
  judgeResult.value = `${judge.status}：${judge.report}`
  judgeCases.value = judge.cases
  activeTab.value = '判题结果'
}

const submitCode = async () => {
  if (userStore.role !== 'student' && userStore.role !== 'teacher') {
    judgeResult.value = '无效用户角色，无法提交'
    return
  }
  await runCode()
  const status = judgeResult.value.includes('AC') ? 'AC' : '提交中'
  submitHistory.unshift({ time: new Date().toLocaleString(), status })
}

const fillDemoAnswer = () => {
  if (language.value === 'Python') {
    code.value = `def solution(nums, target):\n    d = {}\n    for i, v in enumerate(nums):\n        if target - v in d:\n            return [d[target - v], i]\n        d[v] = i`
  } else if (language.value === 'C++') {
    code.value = `#include <vector>\nusing namespace std;\nvector<int> solution(vector<int>& nums, int target) {\n    unordered_map<int, int> map;\n    for (int i = 0; i < nums.size(); i++) {\n        if (map.count(target - nums[i])) return {map[target - nums[i]], i};\n        map[nums[i]] = i;\n    }\n    return {};\n}`
  } else {
    code.value = `function solution(nums, target) {\n  const map = new Map();\n  for (let i = 0; i < nums.length; i++) {\n    const need = target - nums[i];\n    if (map.has(need)) return [map.get(need), i];\n    map.set(nums[i], i);\n  }\n  return [];
}`
  }
}

const isProblemListModalOpen = ref(false)

const openProblemListModal = () => {
  isProblemListModalOpen.value = true
}

const closeProblemListModal = () => {
  isProblemListModalOpen.value = false
}

const resetCode = () => {
  code.value = getDefaultCodeTemplate()
  runLog.value = ''
  judgeResult.value = '尚未运行'
}

const switchProblem = (problemId: string) => {
  router.push({ name: 'workspace', query: { problemId } })
  isProblemListModalOpen.value = false
}
</script>

<style scoped>
.workspace-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #0f172a;
  color: #e2e8f0;
}

.workspace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #1e293b;
}

.workspace-top-left,
.workspace-top-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.problem-select,
.language-select {
  border: 1px solid #334155;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 0.35rem;
  padding: 0.3rem 0.6rem;
}

.btn-sm {
  padding: 0.35rem 0.7rem;
  font-size: 0.78rem;
  border: 1px solid #334155;
  background: #1e293b;
  color: #e2e8f0;
  border-radius: 0.35rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-content {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 0.75rem;
  width: min(90vw, 520px);
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #334155;
}

.modal-body {
  padding: 0.75rem;
  overflow-y: auto;
}

.modal-item {
  border-bottom: 1px solid #1e293b;
}

.modal-item button {
  width: 100%;
  padding: 0.6rem;
  text-align: left;
  color: #cbd5e1;
}

.modal-item button:hover {
  background: #1b2433;
}

.back-btn {
  padding: 0.5rem 1rem;
  background-color: #1e293b;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background-color: #334155;
}

.workspace-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-panel {
  flex: 0 0 40%;
  background-color: #ffffff;
  color: #1e293b;
  border-right: 1px solid #e2e8f0;
  overflow-y: auto;
  padding: 1.5rem;
}

.problem-info h2 {
  margin-top: 0;
}

.resizer {
  width: 4px;
  background-color: #1e293b;
  cursor: col-resize;
  transition: background-color 0.2s;
}

.resizer:hover {
  background-color: #3b82f6;
}

.right-panel {
  flex: 0 0 60%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-section {
  flex: 1;
  padding: 1rem;
  border-bottom: 1px solid #1e293b;
}

.editor-section h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.code-editor {
  width: 100%;
  height: calc(100% - 2rem);
  background-color: #1e293b;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.875rem;
  resize: none;
}

.console-section {
  flex: 0 0 30%;
  border-bottom: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  gap: 0;
  padding: 0;
  border-bottom: 1px solid #334155;
}

.tab-button {
  padding: 0.75rem 1rem;
  background-color: #111827;
  color: #94a3b8;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.tab-button:hover {
  color: #e2e8f0;
}

.tab-button.active {
  background-color: #1e293b;
  color: #e2e8f0;
  border-bottom: 2px solid #3b82f6;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
  background-color: #111827;
}

.tab-pane {
  padding: 1rem;
  color: #94a3b8;
}

.action-buttons {
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-run {
  background-color: #334155;
  color: #e2e8f0;
}

.btn-run:hover {
  background-color: #475569;
}

.btn-submit {
  background-color: #10b981;
  color: #ffffff;
}

.btn-submit:hover {
  background-color: #059669;
}
</style>
