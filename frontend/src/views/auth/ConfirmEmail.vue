<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Подтверждение email</div>
    <div class="info-text" style="position:absolute; left: 50%; top: 400px; transform:translate(-50%, 0); color: white;">
      {{ msg }}
      <div v-if="success">
        <router-link to="/otp-setup" class="div5" style="margin-top:30px; display:inline-block;">Перейти к настройке 2FA</router-link>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, inject } from 'vue'
import { useRoute } from 'vue-router'
// import axios from 'axios'

const api = inject('api')
const msg = ref('Проверяем ссылку...')
const success = ref(false)
const route = useRoute()

onMounted(async () => {
  const uid = route.params.uid
  const token = route.params.token
  try {
    await api.post('/auth/users/activation/', { uid, token })
    msg.value = "Email успешно подтвержден! Теперь настройте двухфакторную аутентификацию."
    success.value = true
  } catch (e) {
    msg.value = e.response?.data?.detail || "Ошибка подтверждения email."
  }
})
</script>
<style scoped>
@import '@/assets/style.css';
.info-text { font-size: 24px; }
</style>
