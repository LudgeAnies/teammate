<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <div class="div4">Завершаем вход через Яндекс</div>-->
<!--    <div style="color:white; text-align:center; margin-top:30px;">{{ msg }}</div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { onMounted, ref, inject } from 'vue'-->
<!--import { useRoute, useRouter } from 'vue-router'-->
<!--import axios from 'axios'-->

<!--const api = inject('api')-->
<!--const msg = ref('Пожалуйста, подождите...')-->
<!--const route = useRoute()-->
<!--const router = useRouter()-->

<!--onMounted(async () => {-->
<!--  const code = route.query.code-->
<!--  const state = route.query.state // если передавал-->

<!--  if (!code) {-->
<!--    msg.value = 'Нет кода авторизации (ошибка авторизации через Яндекс)'-->
<!--    return-->
<!--  }-->
<!--  try {-->
<!--    const redirect_uri = window.location.origin + '/social-auth-complete'-->
<!--    const { data } = await axios.post('/auth/o/yandex-oauth2/', {-->
<!--      code,-->
<!--      redirect_uri-->
<!--    })-->
<!--    // djoser выдаст тебе access_token в data (opaque)-->
<!--    localStorage.setItem('access_token', data.access_token)-->
<!--    router.push({ name: 'otp_verify' }) // нет, мы сначала делаем редиркет на подтверждение почты-->
<!--  } catch (e) {-->
<!--    msg.value = e.response?.data?.detail || 'Ошибка авторизации через Яндекс'-->
<!--  }-->
<!--})-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
