<template>
  <div v-if="show" class="error-display" :class="type">
    <div class="error-header">
      <span class="error-icon">
        <span v-if="type === 'error'">❌</span>
        <span v-if="type === 'warning'">⚠️</span>
        <span v-if="type === 'success'">✅</span>
        <span v-if="type === 'info'">ℹ️</span>
      </span>
      <span class="error-title">{{ title }}</span>
      <button v-if="dismissible" @click="dismiss" class="dismiss-btn">×</button>
    </div>
    <div class="error-content">
      {{ message }}
    </div>
    <div v-if="details" class="error-details">
      <details>
        <summary>详细信息</summary>
        <pre>{{ details }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  error?: Error | string | null
  type?: 'error' | 'warning' | 'success' | 'info'
  title?: string
  dismissible?: boolean
  autoDismiss?: number // 自动消失时间（毫秒）
}

const props = withDefaults(defineProps<Props>(), {
  error: null,
  type: 'error',
  title: '',
  dismissible: true,
  autoDismiss: 0
})

const emit = defineEmits<{
  dismissed: []
}>()

const show = ref(false)
const message = ref('')
const details = ref('')

const updateError = () => {
  if (!props.error) {
    show.value = false
    return
  }

  if (typeof props.error === 'string') {
    message.value = props.error
    details.value = ''
  } else if (props.error instanceof Error) {
    message.value = props.error.message
    details.value = props.error.stack || ''
  } else {
    message.value = String(props.error)
    details.value = ''
  }

  show.value = true

  // 自动消失
  if (props.autoDismiss > 0) {
    setTimeout(() => {
      dismiss()
    }, props.autoDismiss)
  }
}

const dismiss = () => {
  show.value = false
  emit('dismissed')
}

watch(() => props.error, updateError, { immediate: true })
</script>

<style scoped>
.error-display {
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  border: 1px solid;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.error-display.error {
  background-color: #fee;
  border-color: #f66;
  color: #c00;
}

.error-display.warning {
  background-color: #ffd;
  border-color: #fc6;
  color: #960;
}

.error-display.success {
  background-color: #efe;
  border-color: #6c6;
  color: #060;
}

.error-display.info {
  background-color: #eef;
  border-color: #66c;
  color: #006;
}

.error-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 600;
}

.error-icon {
  margin-right: 8px;
  font-size: 18px;
}

.error-title {
  flex: 1;
}

.dismiss-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  padding: 0 8px;
  line-height: 1;
}

.dismiss-btn:hover {
  opacity: 1;
}

.error-content {
  margin-bottom: 8px;
  line-height: 1.5;
}

.error-details {
  margin-top: 8px;
}

.error-details summary {
  cursor: pointer;
  color: inherit;
  opacity: 0.8;
  font-size: 14px;
  user-select: none;
}

.error-details summary:hover {
  opacity: 1;
}

.error-details pre {
  margin: 8px 0 0 0;
  padding: 12px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}
</style>
