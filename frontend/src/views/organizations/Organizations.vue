<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <div class="rectangle-32"></div>
    <div class="rectangle-19"></div>
    <div class="rectangle-78"></div>
    <div class="rectangle-31"></div>
    <div class="rectangle-30"></div>
    <div class="div2">Организации</div>
    <div class="div3">Уведомления</div>
    <div class="vuesax-linear-folder-2">
      <img class="vuesax-linear-folder-22" src="@/assets/img/vuesax-linear-folder-21.svg" />
    </div>
    <div class="activ-menu">
      <img class="vuesax-linear-profile" src="@/assets/img/vuesax-linear-profile0.svg" />
      <img class="vuesax-linear-sms-notification" src="@/assets/img/vuesax-linear-sms-notification0.svg" />
      <img class="group-11" src="@/assets/img/group-110.svg" />
    </div>
    <div class="div4" style="top: 140px;">Ваши организации</div>
    <div v-if="orgs.length === 0" class="div5" style="top: 300px;">
      Вы не состоите ни в одной организации.<br>
      <router-link to="/org-invite" style="color:#1890ff; text-decoration:underline;">Войти по коду</router-link>
    </div>
    <div v-else class="org-list" style="position:absolute; left:300px; top:220px; right:60px;">
      <div v-for="org in orgs" :key="org.id" class="org-card" style="background:#fff; border-radius:18px; margin-bottom:38px; box-shadow:0 2px 8px #1890ff20; display:flex; align-items:center; min-height:120px;">
        <img v-if="org.avatar" :src="org.avatar" alt="avatar" style="width:88px;height:88px;object-fit:cover;border-radius:50%;margin:20px;">
        <img v-else src="@/assets/img/group-90.svg" style="width:88px;height:88px;object-fit:cover;border-radius:50%;margin:20px;">
        <div>
          <div style="font-size:28px; font-weight:700; color:#21313c;">{{ org.name }}</div>
          <div style="font-size:16px; color:#21313c; opacity:.7; margin-top:4px;">{{ org.description }}</div>
          <div style="font-size:14px; color:#1890ff; margin-top:8px;">Роль: <b>{{ roleText(org.role) }}</b></div>
          <router-link :to="`/organization/${org.slug}`" style="font-size:16px; color:#1890ff; margin-top:12px; display:inline-block;">Перейти</router-link>
        </div>
      </div>
    </div>
    <img class="group-9" src="@/assets/img/group-90.svg" />
    <div class="teammate">Teammate</div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
// import { api } from '@/api'

const api = inject('api')
const orgs = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('organizations/my/')
    orgs.value = data
  } catch (e) {
    orgs.value = []
  }
})

function roleText(role) {
  if (role === 'admin') return 'Администратор'
  if (role === 'employee') return 'Сотрудник'
  return role
}
</script>

<style scoped>
@import '@/assets/style.css';
.org-list {
  max-width: 1100px;
}
.org-card {
  transition: box-shadow .2s;
}
.org-card:hover {
  box-shadow:0 4px 24px #1890ff50;
}
</style>
