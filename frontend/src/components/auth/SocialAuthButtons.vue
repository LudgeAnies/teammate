<template>
  <div class="social-auth-container">
    <div class="divider">или войдите с помощью</div>
    <div class="social-buttons">
      <a :href="yandexAuthUrl" class="social-btn">
        <img src="@/assets/img/yandex-icon-svg-10.png" alt="Yandex" />
      </a>
    </div>
  </div>
</template>

<script setup>
const yandexClientId = import.meta.env.VITE_YANDEX_CLIENT_ID;
const redirect = encodeURIComponent("http://localhost:8000/social-auth-complete")
const yandexAuthUrl = 'https://oauth.yandex.ru/authorize?response_type=code&client_id=${yandexClientId}&redirect_uri=${redirect}'
</script>

<!--<script setup>-->

// const yandexClientId = import.meta.env.VITE_YANDEX_CLIENT_ID;
<!--// const callback = "http://localhost:8000/social-auth-complete"-->
<!--//-->
<!--// const yandexAuthUrl = 'https://oauth.yandex.ru/authorize?response_type=code&client_id=${yandexClientId}&redirect_uri=${encodeURIComponent(callback)}'-->

<!--</script>-->

<style scoped>
.social-auth-container {
  width: 100%;
  margin: 30px 0;
  text-align: center;
}

.divider {
  color: white;
  font-size: 16px;
  margin-bottom: 16px;
  position: relative;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.social-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 66px;
  height: 66px;
  border-radius: 50%;
  background: white;
  transition: transform 0.2s;
}

.social-btn:hover {
  transform: scale(1.05);
}

.social-btn img {
  width: 100%;
  height: auto;
}

@media (max-width: 600px) {
  .divider {
    font-size: 14px;
  }

  .divider::before,
  .divider::after {
    width: 25%;
  }

  .social-btn {
    width: 56px;
    height: 56px;
  }
}

</style>
