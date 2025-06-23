<!--<script setup>-->
<!--import { onMounted, ref } from 'vue'-->
<!--import { useRoute, useRouter } from 'vue-router'-->
<!--import axios from 'axios'-->

<!--const msg = ref('...')-->
<!--const route = useRoute()-->
<!--const router = useRouter()-->

<!--onMounted(async () => {-->
<!--  const code = route.query.code-->
<!--  const mode = route.query.mode-->
<!--  if (!code) {-->
<!--    msg.value = 'Нет кода'-->
<!--    return-->
<!--  }-->
<!--  const redirect_uri = window.location.origin + '/social-auth-complete?mode=' + mode-->
<!--  if (mode === 'register') {-->
<!--    // регистрация-->
<!--    const { data } = await axios.post('/api/users/social/yandex/register/', { code, redirect_uri })-->
<!--    if (data.need_email_verify) {-->
<!--      msg.value = 'Подтвердите почту — письмо отправлено!'-->
<!--      // тут можешь сделать редирект или показать кнопку на логин-->
<!--    }-->
<!--  } else {-->
<!--    // логин-->
<!--    const { data } = await axios.post('/api/users/social/yandex/login/', { code, redirect_uri })-->
<!--    if (data.need_email_verify) {-->
<!--      msg.value = 'Подтвердите почту — письмо отправлено!'-->
<!--    } else if (data.temp_token) {-->
<!--      localStorage.setItem('temp_token', data.temp_token)-->
<!--      router.push('/otp-verify')-->
<!--    }-->
<!--  }-->
<!--})-->
<!--</script>-->
