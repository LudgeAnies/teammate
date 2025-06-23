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
    <div class="div4">Начните работу</div>
    <div class="div5">Вы не состоите ни в одной организации.</div>
    <form @submit.prevent="joinOrg">
      <div class="frame-5978" style="top: 590px;">
        <input v-model="inviteCode" placeholder="Код организации" class="div8" style="background:transparent; border:none; outline:none; color:white; width:100%; font-size:20px;" />
      </div>
      <button class="frame-7" style="top: 679px;" type="submit">
        <div class="div6">Войти</div>
      </button>
    </form>
    <div class="div7">Войдите в организацию</div>
    <img class="group-9" src="@/assets/img/group-90.svg" />
    <div class="teammate">Teammate</div>
    <div v-if="msg" style="position:absolute; left:50%; top:760px; transform:translate(-50%,0); color:#21313c; background:white; padding:10px 20px; border-radius:8px; min-width:300px; text-align:center;">
      {{ msg }}
    </div>
  </div>
</template>
<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const api = inject('api')
const inviteCode = ref('')
const msg = ref('')
const router = useRouter()

async function joinOrg() {
  msg.value = ''
  try {
    await api.post('/organizations/invite', { invite_code: inviteCode.value })
    msg.value = 'Вы успешно вошли в организацию!'
    setTimeout(() => router.push('/organizations'), 1500)
  } catch (e) {
    msg.value = e.response?.data?.invite_code?.[0] || e.response?.data?.detail || 'Ошибка! Код неверный.'
  }
}
</script>
<style scoped>
@import '@/assets/style.css';
input.div8::placeholder { color:rgba(255,255,255,0.7); }
</style>
