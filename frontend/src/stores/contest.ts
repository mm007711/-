import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { fetchContests, createContest, type Contest } from '@/api'

export const useContestStore = defineStore('contest', () => {
  const contests = reactive<Contest[]>([])

  const loadContests = async () => {
    try {
      const list = await fetchContests()
      contests.splice(0, contests.length, ...list)
    } catch (error) {
      console.error('加载比赛失败:', error)
      throw error
    }
  }

  const addContest = async (contestData: Omit<Contest, 'id' | 'created_by' | 'created_at'>) => {
    try {
      const newContest = await createContest(contestData)
      contests.push(newContest)
      return newContest
    } catch (error) {
      console.error('创建比赛失败:', error)
      throw error
    }
  }

  const getContest = (id: number) => {
    return contests.find(c => c.id === id)
  }

  return { contests, loadContests, addContest, getContest }
})
