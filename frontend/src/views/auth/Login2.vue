<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/vector-650.svg" />-->
<!--    <img class="vector-64" src="@/assets/vector-640.svg" />-->
<!--    <div class="div4">ВХОД</div>-->
<!--    <form @submit.prevent="login">-->
<!--      <div class="frame-5977"><input v-model="loginStr" placeholder="Email или имя пользователя" class="email" required /></div>-->
<!--      <div class="frame-5980"><input v-model="password" type="password" placeholder="Пароль" class="div3" required /></div>-->
<!--      <div class="frame-5982">-->
<!--        <button type="submit" class="div5" :disabled="pending">Войти</button>-->
<!--      </div>-->
<!--    </form>-->
<!--    <SocialAuthButtons />-->

<!--    <div class="div6">-->
<!--      <span>-->
<!--        <span class="div-6-span">Нет аккаунта?</span>-->
<!--        <router-link class="div-6-span2" to="/register">Зарегистрироваться</router-link>-->
<!--      </span>-->
<!--    </div>-->
<!--    <div v-if="msg" style="color:white; text-align:center; margin-top:20px;">{{ msg }}</div>-->
<!--    <router-link to="/reset-password" style="color:white; display:block; text-align:center; margin-top:20px;">Забыли пароль?</router-link>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import axios from 'axios'-->
<!--import { setToken } from '@/api'-->
<!--import SocialAuthButtons from '@/components/SocialAuthButtons.vue'-->

<!--const router = useRouter()-->
<!--const loginStr = ref('')-->
<!--const password = ref('')-->
<!--const pending = ref(false)-->
<!--const msg = ref('')-->

<!--async function login() {-->
<!--  pending.value = true-->
<!--  msg.value = ''-->
<!--  try {-->
<!--    // OAuth2 Password Grant (django-oauth-toolkit)-->
<!--    const params = new URLSearchParams()-->
<!--    params.append('grant_type', 'password')-->
<!--    params.append('username', loginStr.value)-->
<!--    params.append('password', password.value)-->
<!--    params.append('client_id', '<client_id>')-->
<!--    params.append('client_secret', '<client_secret>')-->
<!--    const { data } = await axios.post('/o/token/', params)-->
<!--    setToken(data.access_token)-->
<!--    router.push('/otp')-->
<!--  } catch (e) {-->
<!--    msg.value = e.response?.data?.error_description || 'Ошибка входа'-->
<!--  } finally {-->
<!--    pending.value = false-->
<!--  }-->
<!--}-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
