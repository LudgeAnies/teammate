<template>
  <div class="register-root">
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

    <div class="registration-container">
      <h1 class="registration-title">РЕГИСТРАЦИЯ</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <input class="input-field" v-model="email" type="email" placeholder="Email" required autocomplete="email" />
        </div>
        <div class="form-group">
          <input class="input-field" v-model="username" type="text" placeholder="Имя пользователя" required autocomplete="username" />
        </div>
        <div class="form-group">
          <input class="input-field" v-model="first_name" type="text" placeholder="Имя" required autocomplete="given-name" />
        </div>
        <div class="form-group">
          <input class="input-field" v-model="last_name" type="text" placeholder="Фамилия" required autocomplete="family-name" />
        </div>
        <div class="form-group">
          <input class="input-field" v-model="password" type="password" placeholder="Пароль" required autocomplete="new-password" />
        </div>
        <div class="form-group">
          <input class="input-field" v-model="password2" type="password" placeholder="Подтвердить пароль" required autocomplete="new-password" />
        </div>
        <button type="submit" class="submit-btn" :disabled="pending">Зарегистрироваться</button>
        <SocialAuthButtons />
      </form>

      <div class="login-link">
        Уже есть аккаунт?
        <router-link to="/login">Войти</router-link>
      </div>
      <div v-if="msg" class="signup-error">
        {{ msg }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import SocialAuthButtons from '@/components/auth/SocialAuthButtons.vue'
import { api } from '@/api/api'

// const api = inject('api')
const router = inject('router', useRouter())
const email = ref('')
const username = ref('')
const first_name = ref('')
const last_name = ref('')
const password = ref('')
const password2 = ref('')
const pending = ref(false)
const msg = ref('')

async function register() {
  if (password.value !== password2.value) {
    msg.value = "Пароли не совпадают"
    return
  }
  pending.value = true
  msg.value = ''
  try {
    await api.post('auth/users/', {
      email: email.value,
      username: username.value,
      first_name: first_name.value,
      last_name: last_name.value,
      password: password.value,
      re_password: password2.value,
    })
    router.push('/login')
  } catch (e) {
    msg.value = Object.values(e.response?.data || {}).flat().join('; ') || 'Ошибка регистрации'
  } finally {
    pending.value = false
  }
}
</script>

<style scoped>
/* Голубой фон для всей страницы */
.register-root, html, body {
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  background: linear-gradient(-74.64deg, rgba(24,144,255,0.9) 0%, rgba(24,144,255,0.9) 100%);
  overflow-x: hidden;
  position: relative;
  font-family: 'Roboto', sans-serif;
}

/* Фоновые svg всегда внутри голубого фона, НЕ мешают адаптиву */
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

/* Регистрационная форма */
.registration-container {
  position: relative;
  z-index: 2;
  max-width: 400px;
  margin: 100px auto 0 auto;
  padding: 40px 32px 32px 32px;
  background: rgba(255,255,255,0.13);
  border-radius: 10px;
  backdrop-filter: blur(24px);
  box-shadow:
    inset 0px 0px 68px 0px rgba(255,255,255,0.07),
    inset 0px 4px 10px 0px rgba(255,255,255,0.18);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* Заголовок */
.registration-title {
  color: #ffffff;
  text-align: center;
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 36px;
  letter-spacing: 1px;
}

.form-group {
  margin-bottom: 20px;
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

a {
  text-decoration: none;
}

.login-link {
  text-align: center;
  margin-top: 30px;
  color: #fff;
  font-size: 18px;
}
.login-link a {
  color: #21313c;
  font-weight: 500;
  margin-left: 5px;
  text-decoration: underline;
}

.yandex-link {
  text-align: center;
  margin-top: 30px;
  color: #fff;
  font-size: 18px;
}
.yandex-link a {
  color: #21313c;
  font-weight: 500;
  margin-left: 5px;
}

.signup-error {
  color: #fa7070;
  text-align: center;
  margin-top: 16px;
  font-size: 1rem;
}

.group-9 {
  height: auto;
  position: absolute;
  left: 17px;
  top: 16px;
  overflow: visible;
}
.teammate {
  color: #000000;
  text-align: left;
  font-family: "Anta-Regular", sans-serif;
  font-size: 18px;
  font-weight: 400;
  position: absolute;
  left: 56px;
  top: 19px;
  width: 96px;
  height: 24px;
}

/* Адаптив */
@media (max-width: 600px) {
  .header {
    padding: 0 6px;
    height: 44px;
  }
  .registration-container {
    max-width: 98vw;
    padding: 16px 3vw;
    margin: 70px auto 0 auto;
    border-radius: 8px;
  }
  .registration-title {
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
  .login-link, .yandex-link {
    font-size: 15px;
  }
  .vector-65 {
    min-width: 280px;
  }
  .vector-64 {
    min-width: 180px;
  }
  .with {
  color: #ffffff;
  text-align: left;
  font-family: "Arima-Regular", sans-serif;
  font-size: 14px;
  font-weight: 400;
  position: absolute;
  left: calc(50% - 86px);
  top: 937px;
}
}
</style>
