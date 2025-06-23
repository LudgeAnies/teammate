import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import '@/assets/style.css'
import { api } from "@/api/api"
import { createPinia } from "pinia"

const app = createApp(App)
const pinia = createPinia()

app.provide('api', api)
app.provide('router', router)

app.use(router)
app.use(pinia)

app.mount('#app')
