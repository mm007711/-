<template>
  <div class="workspace-page">
    <div class="workspace-header">
      <button @click="goBack" class="back-btn">返回大厅</button>
      <h1>{{ currentProblem }}</h1>
    </div>

    <div class="workspace-container">
      <section class="left-panel">
        <div class="problem-info">
          <h2>题目详情</h2>
          <p>题目信息、描述、示例、约束条件等将在这里显示。</p>
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
              :class="{ active: activeTab === tab }"
              class="tab-button"
            >
              {{ tab }}
            </button>
          </div>
          <div class="tab-content">
            <div v-if="activeTab === '测试用例'" class="tab-pane">
              <p>测试用例编辑区</p>
            </div>
            <div v-if="activeTab === '判题结果'" class="tab-pane">
              <p>判题结果显示区</p>
            </div>
            <div v-if="activeTab === '运行日志'" class="tab-pane">
              <p>运行日志输出区</p>
            </div>
            <div v-if="activeTab === '提交历史'" class="tab-pane">
              <p>提交历史记录区</p>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="runCode" class="btn btn-run">运行测试</button>
          <button @click="submitCode" class="btn btn-submit">正式提交</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentProblem = ref('No.1 两数之和')
const code = ref('')
const activeTab = ref('测试用例')
const consoleTabs = ['测试用例', '判题结果', '运行日志', '提交历史']

const goBack = () => {
  // 返回大厅逻辑
  console.log('返回大厅')
}

const runCode = () => {
  // 运行测试逻辑
  console.log('运行测试', code.value)
}

const submitCode = () => {
  // 正式提交逻辑
  console.log('正式提交', code.value)
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
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #1e293b;
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
