import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { me, login as apiLogin, register as apiRegister, type User } from '@/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = reactive<{
    data: User | null
    loading: boolean
    error: string | null
  }>({
    data: null,
    loading: false,
    error: null
  })

  const isAuthenticated = () => {
    return currentUser.data !== null && localStorage.getItem('codeedu_token') !== null
  }

  const isTeacher = () => {
    return currentUser.data?.role === 'teacher' || currentUser.data?.role === 'admin'
  }

  const isAdmin = () => {
    return currentUser.data?.role === 'admin'
  }

  const isStudent = () => {
    return currentUser.data?.role === 'student'
  }

  const loadCurrentUser = async () => {
    currentUser.loading = true
    currentUser.error = null
    
    try {
      const token = localStorage.getItem('codeedu_token')
      if (!token) {
        throw new Error('未登录')
      }
      
      const userData = await me()
      currentUser.data = userData
    } catch (error) {
      currentUser.error = error instanceof Error ? error.message : '加载用户信息失败'
      localStorage.removeItem('codeedu_token')
      currentUser.data = null
    } finally {
      currentUser.loading = false
    }
  }

  const login = async (username: string, password: string) => {
    currentUser.loading = true
    currentUser.error = null
    
    try {
      await apiLogin(username, password)
      await loadCurrentUser()
    } catch (error) {
      currentUser.error = error instanceof Error ? error.message : '登录失败'
      throw error
    } finally {
      currentUser.loading = false
    }
  }

  const register = async (username: string, password: string) => {
    currentUser.loading = true
    currentUser.error = null
    
    try {
      await apiRegister(username, password)
      await login(username, password)
    } catch (error) {
      currentUser.error = error instanceof Error ? error.message : '注册失败'
      throw error
    } finally {
      currentUser.loading = false
    }
  }

  const logout = () => {
    localStorage.removeItem('codeedu_token')
    currentUser.data = null
    currentUser.error = null
  }

  // 初始化时尝试加载用户
  const init = async () => {
    const token = localStorage.getItem('codeedu_token')
    if (token) {
      await loadCurrentUser()
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isTeacher,
    isAdmin,
    isStudent,
    loadCurrentUser,
    login,
    register,
    logout,
    init
  }
})
