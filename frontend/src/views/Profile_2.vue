<!--<template>-->
<!--  <div class="div">-->
<!--    <div class="rectangle-77"></div>-->
<!--    <img class="vector-65" src="@/assets/img/vector-650.svg" />-->
<!--    <div class="div4">Личный кабинет</div>-->
<!--    <div style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); color:#21313c; background:rgba(255,255,255,0.98); padding:40px 60px; border-radius:16px; box-shadow:0 2px 16px #0002;">-->
<!--      <div v-if="user">-->
<!--        <div style="font-size:26px;"><b>{{ user.first_name }} {{ user.last_name }}</b></div>-->
<!--        <div style="font-size:18px; margin-top:12px;">Email: <b>{{ user.email }}</b></div>-->
<!--        <div style="font-size:18px; margin-top:12px;">Имя пользователя: <b>{{ user.username }}</b></div>-->
<!--      </div>-->
<!--      <button class="div5" @click="logout" style="margin-top:32px;">Выйти</button>-->
<!--      <router-link to="/org-invite" style="display:block; margin-top:24px; color:#1890ff; font-weight:bold;">Войти в организацию по коду</router-link>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import { api, clearToken } from '@/api/api'-->

<!--const user = ref(null)-->
<!--const router = useRouter()-->

<!--onMounted(async () => {-->
<!--  const { data } = await api.get('users/me/')-->
<!--  user.value = data-->
<!--})-->

<!--function logout() {-->
<!--  clearToken()-->
<!--  router.push('/login')-->
<!--}-->
<!--</script>-->
<!--<style scoped>-->
<!--@import '@/assets/style.css';-->
<!--</style>-->
