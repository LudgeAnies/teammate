<script>
export default {
  name: 'App'
}
</script>

<template>
  <div id="app">
    <div class="background-elements">
      <img class="vector-65" src="@/assets/img/vector-650.svg" alt="">
      <img class="vector-64" src="@/assets/img/vector-640.svg" alt="">
    </div>
    <router-view />
  </div>
</template>

<style scoped>
@import '@/assets/style2.css';
</style>