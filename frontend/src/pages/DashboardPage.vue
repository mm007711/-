<template>
  <div class="dashboard-page">
    <h1>大厅 (Dashboard)</h1>
    <div class="tabs">
      <div class="tab">
        <h2>公共题库</h2>
        <p>教师可发布新题；发布比赛/测验时，可直接从这里勾题组卷。</p>
      </div>
      <div class="tab">
        <h2>编程比赛/测验</h2>
        <p>教师可从公共题库勾题，也可额外导入 JSON 题目后直接纳入本场测试。</p>
      </div>
      <div class="tab">
        <h2>班级成绩管理</h2>
        <p>支持导入学生名单与导出 CSV 成绩单。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dashboard 页面逻辑
// 包含：题库表格、比赛列表、班级管理
</script>

<style scoped>
.dashboard-page {
  padding: 2rem;
}

.tabs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.tab {
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.tab h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.tab p {
  margin: 0;
  color: #64748b;
  font-size: 0.875rem;
}
</style>
