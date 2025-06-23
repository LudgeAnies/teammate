<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/vector-650.svg" />-->
<!--    <div class="div4">Двухфакторная аутентификация</div>-->
<!--    <div class="otp-instruction" style="position:absolute; left: 50%; top: 400px; transform:translate(-50%, 0); color: white; text-align:center;">-->
<!--      <div>Отсканируйте QR-код в вашем приложении (Google Authenticator, Indeed Key и т.п.)</div>-->
<!--      <img v-if="qrCode" :src="`data:image/png;base64,${qrCode}`" style="margin: 24px auto; display: block; max-width: 300px;" />-->
<!--      <div v-if="secretKey" style="margin: 10px 0;">Или введите секретный ключ вручную: <b style="color:#fff">{{ secretKey }}</b></div>-->
<!--      <router-link to="/otp" class="div5" style="margin-top: 24px; display:inline-block;">Ввести код</router-link>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { api } from '@/api'-->

<!--const qrCode = ref('')-->
<!--const secretKey = ref('')-->

<!--onMounted(async () => {-->
<!--  try {-->
<!--    const { data } = await api.get('users/otp-setup/')-->
<!--    qrCode.value = data.qr_code-->
<!--    secretKey.value = data.secret_key-->
<!--  } catch (e) {-->
<!--    // ошибка отображается по-своему, если нужно-->
<!--  }-->
<!--})-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--.otp-instruction { font-size: 20px; }-->
<!--</style>-->
