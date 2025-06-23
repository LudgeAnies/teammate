<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/img/vector-650.svg" />-->
<!--    <img class="vector-64" src="@/assets/img/vector-640.svg" />-->
<!--    <div class="div4">ВХОД</div>-->
<!--    <form @submit.prevent="login">-->
<!--      <div class="frame-5977">-->
<!--        <input v-model="loginStr" placeholder="Email или имя пользователя" class="email" required />-->
<!--      </div>-->
<!--      <div class="frame-5980">-->
<!--        <input v-model="password" type="password" placeholder="Пароль" class="div3" required />-->
<!--      </div>-->
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
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref, inject } from 'vue'-->
<!--import axios from 'axios'-->
<!--import { useRouter } from 'vue-router'-->
<!--import SocialAuthButtons from '@/components/auth/SocialAuthButtons.vue'-->

<!--const api = inject('api')-->
<!--const loginStr = ref('')-->
<!--const password = ref('')-->
<!--const pending = ref(false)-->
<!--const msg = ref('')-->
<!--// const router = useRouter() // дефолтный вариант-->
<!--const router = inject('router', useRouter()) // fallback на стандартный useRouter()-->

<!--async function login() {-->
<!--  pending.value = true-->
<!--  msg.value = ''-->
<!--  try {-->
<!--    // POST login (шаг 1): username+password, ждём temp_token-->
<!--    const { data } = await api.post('/users/login/', {-->
<!--      username: loginStr.value,-->
<!--      password: password.value,-->
<!--    })-->
<!--    // temp_token сохранен в localStorage/sessionStorage или store-->
<!--    localStorage.setItem('temp_token', data.temp_token)-->
<!--    router.push({ name: 'otp_verify' })-->
<!--  } catch (e) {-->
<!--    msg.value = e.response?.data?.detail || 'Ошибка входа'-->
<!--  } finally {-->
<!--    pending.value = false-->
<!--  }-->
<!--}-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
