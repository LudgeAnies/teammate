<template>
  <div class="div">
    <div class="rectangle-77"></div>
    <img class="vector-65" src="@/assets/img/vector-650.svg" />
    <div class="div4">Личный кабинет</div>
    <div
      style="position:absolute; left:50%; top:400px; transform:translate(-50%, 0); color:#21313c; background:rgba(255,255,255,0.98); padding:40px 60px; border-radius:16px; box-shadow:0 2px 16px #0002;">
      <form v-if="user" @submit.prevent="saveProfile" style="display:flex; flex-direction:column; gap:18px;">
        <div style="font-size:26px;">
          <b>{{ user.first_name }} {{ user.last_name }}</b>
        </div>
        <div style="font-size:18px;">
          Email: <b>{{ user.email }}</b>
        </div>
        <div style="font-size:18px;">
          Имя пользователя: <b>{{ user.username }}</b>
        </div>

        <div style="margin-top:16px;">
          <label>Имя:</label>
          <input v-model="editForm.first_name" type="text" class="form-control" style="width:220px;" />
        </div>
        <div>
          <label>Фамилия:</label>
          <input v-model="editForm.last_name" type="text" class="form-control" style="width:220px;" />
        </div>
        <div>
          <label>Фото (аватар):</label>
          <input type="file" accept="image/*" @change="onAvatarChange" />
          <div v-if="user.avatar" style="margin-top:8px;">
            <img :src="user.avatar" alt="avatar" style="max-width:90px; max-height:90px; border-radius:50%;" />
          </div>
        </div>
        <button type="submit" class="div5" style="margin-top:12px;">Сохранить</button>
      </form>
      <div v-if="successMsg" style="color: #1890ff; margin-top: 12px;">{{ successMsg }}</div>
      <button class="div5" @click="logout" style="margin-top:32px;">Выйти</button>
      <router-link to="/org-invite" style="display:block; margin-top:24px; color:#1890ff; font-weight:bold;">
        Войти в организацию по коду
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, clearToken } from '@/api/api'

const user = ref(null)
const editForm = ref({
  first_name: '',
  last_name: '',
  avatar: null,
})
const successMsg = ref('')
const router = useRouter()

onMounted(async () => {
  const { data } = await api.get('users/me/')
  user.value = data
  editForm.value.first_name = data.first_name || ''
  editForm.value.last_name = data.last_name || ''
})

function onAvatarChange(e) {
  const file = e.target.files[0]
  editForm.value.avatar = file
}

async function saveProfile() {
  const formData = new FormData()
  formData.append('first_name', editForm.value.first_name)
  formData.append('last_name', editForm.value.last_name)
  if (editForm.value.avatar) {
    formData.append('avatar', editForm.value.avatar)
  }

  try {
    const { data } = await api.patch('users/me/update/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    user.value.first_name = data.first_name
    user.value.last_name = data.last_name
    if (data.avatar) user.value.avatar = data.avatar
    successMsg.value = 'Данные обновлены'
    setTimeout(() => (successMsg.value = ''), 2500)
  } catch (err) {
    successMsg.value = 'Ошибка при сохранении'
  }
}

function logout() {
  clearToken()
  router.push('/login')
}
</script>
<style scoped>
@import '@/assets/style.css';
.form-control {
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 18px;
  background: #fff;
  margin-top: 2px;
}
</style>
