import { reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import { fetchClasses, createClass, enrollStudent, type Class, type ClassEnrollment, type User } from '@/api'

export const useClassStore = defineStore('class', () => {
  const classes = reactive<Class[]>([])
  const enrollments = reactive<ClassEnrollment[]>([])

  const loadClasses = async () => {
    try {
      const list = await fetchClasses()
      classes.splice(0, classes.length, ...list)
    } catch (error) {
      console.error('加载班级失败:', error)
      throw error
    }
  }

  const addClass = async (classData: Omit<Class, 'id' | 'teacher_id' | 'created_at'>) => {
    try {
      const newClass = await createClass(classData)
      classes.push(newClass)
      return newClass
    } catch (error) {
      console.error('创建班级失败:', error)
      throw error
    }
  }

  const addEnrollment = async (classId: number, studentId: number) => {
    try {
      const enrollment = await enrollStudent(classId, studentId)
      enrollments.push(enrollment)
      return enrollment
    } catch (error) {
      console.error('注册学生失败:', error)
      throw error
    }
  }

  const getClassStudents = (classId: number): ClassEnrollment[] => {
    return enrollments.filter(e => e.class_id === classId)
  }

  const stats = computed(() => {
    const totalClasses = classes.length
    const totalEnrollments = enrollments.length
    
    const avgScore = totalEnrollments > 0 
      ? (enrollments.reduce((sum, e) => sum + e.score, 0) / totalEnrollments).toFixed(1)
      : '0.0'
    
    const activeStudents = enrollments.filter(e => e.solved_count > 0).length
    const activityRate = totalEnrollments > 0 
      ? `${Math.round((activeStudents / totalEnrollments) * 100)}%`
      : '0%'

    return {
      totalClasses,
      totalEnrollments,
      avgScore,
      activityRate,
      activeStudents
    }
  })

  return { 
    classes, 
    enrollments, 
    loadClasses, 
    addClass, 
    addEnrollment, 
    getClassStudents, 
    stats 
  }
})
