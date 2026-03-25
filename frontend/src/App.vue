<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
const isTeacher = computed(() => userStore.role === 'teacher')
const showLoginModal = ref(false)
const loginUser = ref('teacher')
const loginPassword = ref('teacher123')
const loginError = ref('')

onMounted(async () => {
  await userStore.fetchProfile()
})

const tryLogin = async () => {
  loginError.value = ''
  try {
    await userStore.login(loginUser.value, loginPassword.value)
    showLoginModal.value = false
  } catch (error: any) {
    loginError.value = error?.message || '登录失败'
  }
}

const logout = () => {
  userStore.logout()
}
</script>

<template>
  <header class="app-header">
    <div class="brand">
      <img alt="CodeEdu" class="logo" src="@/assets/logo.svg" width="56" height="56" />
      <div>
        <h1>CodeEdu</h1>
        <p>在线编程教学平台</p>
      </div>
    </div>

    <nav>
      <RouterLink to="/" class="nav-link">大厅</RouterLink>
      <RouterLink to="/workspace" class="nav-link">工作区</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </nav>

    <div class="role-switcher">
      <span class="role-tag">当前身份：{{ userStore.isAuthenticated ? userStore.name : '未登录' }}</span>
      <template v-if="userStore.isAuthenticated">
        <button class="login-btn" @click="logout">退出</button>
      </template>
      <template v-else>
        <button class="login-btn" @click="showLoginModal = true">登陆</button>
      </template>
    </div>

    <div v-if="showLoginModal" class="login-modal">
      <div class="login-card">
        <h3>登录</h3>
        <label>用户名</label>
        <input v-model="loginUser" type="text" />
        <label>密码</label>
        <input v-model="loginPassword" type="password" />
        <p class="error" v-if="loginError">{{ loginError }}</p>
        <div class="login-actions">
          <button class="btn btn-sm" @click="tryLogin">确认</button>
          <button class="btn btn-sm" @click="showLoginModal = false">取消</button>
        </div>
      </div>
    </div>
  </header>

  <main class="app-main">
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #0f172a;
  color: #fff;
  padding: 0.8rem 1.5rem;
  border-bottom: 1px solid #1e293b;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.brand h1 {
  margin: 0;
  font-size: 1.1rem;
}
.brand p {
  margin: 0;
  font-size: 0.82rem;
  color: #a5b4fc;
}
.nav-link {
  margin-left: 0.8rem;
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 500;
}
.nav-link.router-link-active {
  color: #fff;
  border-bottom: 2px solid #60a5fa;
}
.role-switcher {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #cbd5e1;
  font-size: 0.8rem;
}
.role-tag {
  font-weight: 500;
}
.role-select {
  background: #1f2937;
  color: #e5e7eb;
  border: 1px solid #374151;
  border-radius: 0.375rem;
  padding: 0.2rem 0.45rem;
}
.role-tip {
  color: #34d399;
  font-weight: 600;
}
.login-btn {
  padding: 0.35rem 0.8rem;
  border: 1px solid #cbd5e1;
  background: #1d4ed8;
  color: white;
  border-radius: 0.4rem;
  cursor: pointer;
}
.login-modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.7);
  z-index: 100;
}
.login-card {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 0.75rem;
  padding: 1rem;
  width: min(95vw, 340px);
}
.login-card input {
  width: 100%;
  padding: 0.4rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.35rem;
  margin-bottom: 0.6rem;
}
.login-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}
.error {
  color: #dc2626;
  font-size: 0.82rem;
}
.app-main {
  min-height: calc(100vh - 72px);
  background: #f8fafc;
}
</style>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
