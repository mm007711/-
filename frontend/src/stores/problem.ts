import { computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import { fetchProblems, getProblem, type Problem } from '@/api'

export const useProblemStore = defineStore('problem', () => {
  const problems = reactive<Problem[]>([])
  const selectedProblemId = reactive({ value: 0 })

  const easyCount = computed(() => problems.filter(p => p.difficulty === '简单' || p.difficulty === 'easy').length)
  const mediumCount = computed(() => problems.filter(p => p.difficulty === '中等' || p.difficulty === 'medium').length)
  const hardCount = computed(() => problems.filter(p => p.difficulty === '困难' || p.difficulty === 'hard').length)

  const stats = computed(() => ({
    total: problems.length,
    easy: easyCount.value,
    medium: mediumCount.value,
    hard: hardCount.value,
  }))

  const loadProblems = async () => {
    try {
      const list = await fetchProblems()
      problems.splice(0, problems.length, ...list)
    } catch (error) {
      console.error('加载题目失败:', error)
      throw error
    }
  }

  const loadProblem = async (id: number) => {
    try {
      return await getProblem(id)
    } catch (error) {
      console.error(`加载题目 ${id} 失败:`, error)
      throw error
    }
  }

  const select = (id: number) => {
    selectedProblemId.value = id
  }

  const current = computed(() => {
    if (selectedProblemId.value === 0 && problems.length > 0) {
      return problems[0]
    }
    return problems.find(p => p.id === selectedProblemId.value) || problems[0]
  })

  const pick = (id: number) => {
    selectedProblemId.value = id
    return current.value
  }

  const add = (p: Problem) => {
    problems.push(p)
  }

  const update = (id: number, p: Problem) => {
    const index = problems.findIndex(problem => problem.id === id)
    if (index !== -1) {
      problems[index] = p
    }
  }

  const remove = (id: number) => {
    const index = problems.findIndex(problem => problem.id === id)
    if (index !== -1) {
      problems.splice(index, 1)
    }
  }

  return { 
    problems, 
    selectedProblemId, 
    loadProblems, 
    loadProblem,
    select, 
    current, 
    pick, 
    add,
    update,
    remove,
    stats 
  }
})
