<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Настройка 2FA</div>
    <div style="position:absolute; left:50%; top:360px; transform:translate(-50%, 0); width:420px; text-align:center;">
      <div style="color: black; font-size:18px;">
        Отсканируйте QR-код или введите секрет вручную в приложении (Google Authenticator, Яндекс.Ключ и т.д.)
      </div>
      <img v-if="qrCode" :src="`data:image/png;base64,${qrCode}`" style="margin: 24px auto; display: block; max-width: 220px;" />
      <div style="color:#fff; font-size:18px; margin-top:12px;">
        Секрет: <b style="font-family:monospace">{{ secret }}</b>
      </div>
      <router-link to="/login" class="div5" style="margin-top:36px; display:inline-block;">Перейти ко входу</router-link>
      <div v-if="msg" style="color:white; margin-top:20px;">{{ msg }}</div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, inject } from 'vue'
const api = inject('api')
const qrCode = ref('')
const secret = ref('')
const msg = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/users/auth/otp/setup/')
    qrCode.value = data.qr_code
    secret.value = data.secret
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка загрузки данных'
  }
})
</script>
<style scoped>
@import '@/assets/style.css';
</style>
