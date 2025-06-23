<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/vector-650.svg" />-->
<!--    <div class="div4">Введите код из приложения</div>-->
<!--    <form @submit.prevent="verifyOtp" style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); text-align:center;">-->
<!--      <input v-model="otp" maxlength="6" class="div3" placeholder="6-значный код" required style="font-size:28px; width:180px; text-align:center; letter-spacing:8px;" />-->
<!--      <button type="submit" class="div5" style="margin-left:16px;">Подтвердить</button>-->
<!--    </form>-->
<!--    <div v-if="msg" style="color:white; text-align:center; margin-top:60px;">{{ msg }}</div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import { api } from '@/api'-->

<!--const router = useRouter()-->
<!--const otp = ref('')-->
<!--const msg = ref('')-->

<!--async function verifyOtp() {-->
<!--  msg.value = ''-->
<!--  try {-->
<!--    await api.post('/users/otp-verify/', { otp: otp.value })-->
<!--    router.push('/profile')-->
<!--  } catch (e) {-->
<!--    msg.value = e.response?.data?.detail || 'Ошибка подтверждения'-->
<!--  }-->
<!--}-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
