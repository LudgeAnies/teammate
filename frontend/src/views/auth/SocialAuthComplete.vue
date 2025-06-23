<template>
  <div style="text-align:center; margin-top:140px;">
    <h2>Авторизация через Яндекс ID...</h2>
    <div v-if="msg">{{ msg }}</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const msg = ref('')
const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const code = route.query.code
  // const state = route.query.state
  // const savedState = localStorage.getItem("oauth_state")

  if (!code) {
    msg.value = 'Нет кода авторизации'
    return
  }
  // if (!state || state !== savedState) {
  //   msg.value = 'Ошибка безопасности: параметр state не совпадает'
  //   return
  // }

  try {
    const { data } = await axios.post('/api/auth/social/yandex/', {
      code,
      redirect_uri: window.location.origin + '/social-auth-complete',
    })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    router.push('/profile')
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка авторизации через Яндекс. Обратитесь к системному администратору.'
  }
})
</script>
