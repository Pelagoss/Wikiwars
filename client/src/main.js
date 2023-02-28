import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import './style.scss'
import App from './App.vue'
import axios from "axios"

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)
const app = createApp(App);

axios.defaults.baseURL = "http://127.0.0.1:5000/";

app.use(pinia);

app.mount('#app');
