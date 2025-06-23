<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/img/vector-650.svg" />-->
<!--    <img class="vector-64" src="@/assets/img/vector-640.svg" />-->
<!--    <div class="div4">РЕГИСТРАЦИЯ</div>-->

<!--    <form @submit.prevent="register">-->
<!--      <div class="frame-5977"><input v-model="email" type="email" placeholder="Email" class="email" required /></div>-->
<!--      <div class="frame-5978"><input v-model="username" placeholder="Имя пользователя" class="div3" required /></div>-->
<!--      <div class="frame-5979"><input v-model="first_name" placeholder="Имя" class="div3" required /></div>-->
<!--      <div class="frame-5983"><input v-model="last_name" placeholder="Фамилия" class="div3" required /></div>-->
<!--      <div class="frame-5980"><input v-model="password" type="password" placeholder="Пароль" class="div3" required /></div>-->
<!--      <div class="frame-5981"><input v-model="password2" type="password" placeholder="Подтвердить пароль" class="div3" required /></div>-->
<!--      <div class="frame-5982">-->
<!--        <button type="submit" class="div5" :disabled="pending">Зарегистрироваться</button>-->
<!--      </div>-->
<!--    </form>-->
<!--    <SocialAuthButtons />-->
<!--    <div class="div6">-->
<!--      <span>-->
<!--        <span class="div-6-span">Уже есть аккаунт?</span>-->
<!--        <router-link class="div-6-span2" to="/login">Войти</router-link>-->
<!--      </span>-->
<!--    </div>-->
<!--    <div v-if="msg" style="color:white; text-align:center; margin-top:20px;">{{ msg }}</div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref, inject } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!-- // import { api } from '@/api'-->

<!--import SocialAuthButtons from '@/components/SocialAuthButtons.vue'-->

<!--const api = inject('api')-->
<!--// const router = useRouter()-->
<!--const router = inject('router', useRouter())-->
<!--const email = ref('')-->
<!--const username = ref('')-->
<!--const first_name = ref('')-->
<!--const last_name = ref('')-->
<!--const password = ref('')-->
<!--const password2 = ref('')-->
<!--const pending = ref(false)-->
<!--const msg = ref('')-->

<!--async function register() {-->
<!--  if (password.value !== password2.value) {-->
<!--    msg.value = "Пароли не совпадают"-->
<!--    return-->
<!--  }-->
<!--  pending.value = true-->
<!--  msg.value = ''-->
<!--  try {-->
<!--    await api.post('users/register/', {-->
<!--      email: email.value,-->
<!--      username: username.value,-->
<!--      first_name: first_name.value,-->
<!--      last_name: last_name.value,-->
<!--      password: password.value,-->
<!--    })-->
<!--    router.push('/email-verification-sent')-->
<!--  } catch (e) {-->
<!--    msg.value = e.response?.data?.detail || 'Ошибка регистрации'-->
<!--  } finally {-->
<!--    pending.value = false-->
<!--  }-->
<!--}-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
