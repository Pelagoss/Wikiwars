import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import './assets/style/tailwind.scss'
import './assets/style/style.scss'
import './utils/vee-validate'
import App from './App.vue'
import {$axios} from "./utils/axios"
import router from "./router";

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)

const app = createApp(App);

app.use(pinia);
app.use(router);
app.provide('axios', $axios);

app.mount('#app');
