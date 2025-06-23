<template>
  <div class="auth-root">

    <div class="background-elements">
      <img class="vector-65" src="@/assets/img/vector-650.svg" alt="">
      <img class="vector-64" src="@/assets/img/vector-640.svg" alt="">
    </div>

    <header class="header">
      <div class="logo">
        <img class="group-9" src="@/assets/img/group-90.svg" alt="Логотип" />
        <span class="teammate">Teammate</span>
      </div>
      <div class="activ-menu">
        <img class="vuesax-linear-profile" src="@/assets/img/vuesax-linear-profile0.svg" alt="Профиль">
        <img class="vuesax-linear-sms-notification" src="@/assets/img/vuesax-linear-sms-notification0.svg" alt="Уведомления">
        <img class="group-11" src="@/assets/img/group-110.svg" alt="Меню">
      </div>
    </header>

    <main class="auth-content">
      <div class="auth-container">
        <h1 class="auth-title">ВХОД</h1>
        <form @submit.prevent="login" class="auth-form">
          <div class="form-group">
            <input
              v-model="loginStr"
              class="input-field"
              placeholder="Email или имя пользователя"
              required
            />
          </div>
          <div class="form-group">
            <input
              v-model="password"
              type="password"
              class="input-field"
              placeholder="Пароль"
              required
            />
          </div>
          <button type="submit" class="submit-btn" :disabled="pending">
            Войти
          </button>
        </form>

        <SocialAuthButtons />

        <div class="auth-link">
          Нет аккаунта?
          <router-link to="/register">Зарегистрироваться</router-link>
        </div>

        <div v-if="msg" class="auth-error">
          {{ msg }}
        </div>
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import SocialAuthButtons from '@/components/auth/SocialAuthButtons.vue'
import { api } from '@/api/api'

const loginStr = ref('')
const password = ref('')
const pending = ref(false)
const msg = ref('')
const router = inject('router', useRouter())

async function login() {
  pending.value = true
  msg.value = ''
  try {
    const { data } = await api.post('/auth/custom-login/', {
      login: loginStr.value,
      password: password.value,
    })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    router.push('/profile')
  } catch (e) {
    msg.value = e.response?.data?.detail || 'Ошибка входа'
  } finally {
    pending.value = false
  }
}
</script>
<style scoped>

/* Общие стили для auth-страниц */
.auth-root, html, body {
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  background: linear-gradient(-74.64deg, rgba(24,144,255,0.9) 0%, rgba(24,144,255,0.9) 100%);
  overflow-x: hidden;
  position: relative;
  font-family: 'Roboto', sans-serif;
}

.background-elements {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.vector-65 {
  position: absolute;
  right: 0; top: 0;
  height: 100vh;
  max-width: 100vw;
  min-width: 500px;
  opacity: 0.7;
  z-index: 1;
}

.vector-64 {
  position: absolute;
  right: 0; bottom: 0;
  height: 50vh;
  max-width: 100vw;
  min-width: 400px;
  opacity: 0.7;
  z-index: 1;
}

/* Header */
.header {
  background: #e2f1ff;
  height: 60px;
  width: 100vw;
  min-width: 320px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 10;
  box-sizing: border-box;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img.group-9 {
  height: 27px;
  width: auto;
  display: block;
}

.activ-menu {
  display: flex;
  gap: 22px;
  align-items: center;
}

.activ-menu img {
  width: 24px; height: 24px;
  display: block;
}

/* Основной контент */
.auth-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
  padding: 60px 20px 40px;
  box-sizing: border-box;
  position: relative;
  z-index: 2;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 40px 32px;
  background: rgba(255,255,255,0.13);
  border-radius: 10px;
  backdrop-filter: blur(24px);
  box-shadow:
    inset 0px 0px 68px 0px rgba(255,255,255,0.07),
    inset 0px 4px 10px 0px rgba(255,255,255,0.18);
}

.auth-title {
  color: #ffffff;
  text-align: center;
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 36px;
  letter-spacing: 1px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  margin-bottom: 0;
}

.input-field {
  width: 100%;
  padding: 14px;
  background: rgba(33, 49, 60, 0.1);
  border-radius: 10px;
  color: rgba(255,255,255,0.7);
  font-size: 20px;
  border: none;
  box-shadow:
    inset 0px 0px 68px 0px rgba(0,0,0,0.05),
    inset 0px 4px 4px 0px rgba(0,0,0,0.15);
  outline: none;
  transition: box-shadow 0.2s;
}

.input-field::placeholder {
  color: rgba(255,255,255,0.7);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #fff;
  border-radius: 10px;
  color: #1890ff;
  font-size: 24px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  margin-top: 20px;
  transition: background 0.15s, color 0.15s;
}

.submit-btn[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
  background: #e6e6e6;
  color: #a6c9e9;
}

.auth-link {
  text-align: center;
  margin-top: 30px;
  color: #fff;
  font-size: 18px;
}

.auth-link a {
  color: #21313c;
  font-weight: 500;
  margin-left: 5px;
  text-decoration: underline;
}

.auth-error {
  color: #fa7070;
  text-align: center;
  margin-top: 16px;
  font-size: 1rem;
}

/* Адаптив */
@media (max-width: 600px) {
  .header {
    padding: 0 6px;
    height: 44px;
  }

  .auth-container {
    max-width: 98vw;
    padding: 30px 20px;
    margin-top: 20px;
    border-radius: 8px;
  }

  .auth-title {
    font-size: 24px;
    margin-bottom: 22px;
  }

  .input-field {
    font-size: 16px;
    padding: 10px;
  }

  .submit-btn {
    font-size: 18px;
    padding: 10px;
  }

  .auth-link {
    font-size: 15px;
  }

  .vector-65 {
    min-width: 280px;
  }

  .vector-64 {
    min-width: 180px;
  }
}

</style>
