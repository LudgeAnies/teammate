<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Двухфакторная аутентификация</div>
    <form @submit.prevent="verifyOtp" style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); text-align:center;">
      <input v-model="otp" maxlength="6" class="div3" placeholder="Код 2FA" required style="font-size:28px; width:180px; text-align:center; letter-spacing:8px;" />
      <button type="submit" class="div5" style="margin-left:16px;">Войти</button>
    </form>
    <div v-if="msg" style="color:white; text-align:center; margin-top:60px;">{{ msg }}</div>
  </div>
</template>
<script setup>
import { ref, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const api = inject('api')
const otp = ref('')
const msg = ref('')
const router = useRouter()

async function verifyOtp() {
  msg.value = ''
  try {
    const temp_token = localStorage.getItem('temp_token')
    const { data } = await api.post('/users/auth/otp/verify', {
      temp_token,
      otp: otp.value,
    })
    localStorage.removeItem('temp_token')
    localStorage.setItem('access_token', data.access_token)
    router.push('/profile')
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка подтверждения'
  }
}
</script>
<style scoped>
@import '@/assets/style.css';
</style>
