<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Восстановление пароля</div>
    <form @submit.prevent="sendReset" style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); text-align:center;">
      <input v-model="email" type="email" placeholder="Email" class="email" required style="font-size:20px; width:300px;"/>
      <button type="submit" class="div5" style="margin-top:24px;">Отправить ссылку</button>
    </form>
    <div v-if="msg" style="color:white; text-align:center; margin-top:60px;">{{ msg }}</div>
    <router-link to="/login" style="color:white; display:block; text-align:center; margin-top:20px;">Вернуться к входу</router-link>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { api } from '@/api/api'

const email = ref('')
const msg = ref('')

async function sendReset() {
  msg.value = ''

  if (!email.value.includes('@')) {
  msg.value = 'Некорректный email';
  return;
}

  try {
    await api.post('users/password-reset/', { email: email.value })
    msg.value = "Если email найден, ссылка для восстановления отправлена"
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка отправки'
  }
}
</script>
<style scoped>
@import '@/assets/style.css';
</style>
