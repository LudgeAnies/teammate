<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Новый пароль</div>
    <form @submit.prevent="reset" style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); text-align:center;">
      <input v-model="password" type="password" placeholder="Новый пароль" class="div3" required style="font-size:20px; width:300px;"/>
      <input v-model="password2" type="password" placeholder="Повторите пароль" class="div3" required style="font-size:20px; width:300px; margin-top:12px;"/>
      <button type="submit" class="div5" style="margin-top:24px;">Сменить пароль</button>
    </form>
    <div v-if="msg" style="color:white; text-align:center; margin-top:60px;">{{ msg }}</div>
    <router-link to="/login" style="color:white; display:block; text-align:center; margin-top:20px;">Войти</router-link>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/api'

const password = ref('')
const password2 = ref('')
const msg = ref('')
const route = useRoute()
const router = useRouter()

async function reset() {
  msg.value = ''
  if (password.value !== password2.value) {
    msg.value = "Пароли не совпадают"
    return
  }
  try {
    const { uid, token } = route.query
    await api.post('users/password-reset/confirm/', {
      uid, token, new_password: password.value
    })
    msg.value = "Пароль успешно изменён"
    setTimeout(() => router.push('/login'), 2000)
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка сброса'
  }
}
</script>
<style scoped>
@import '@/assets/style.css';
</style>
