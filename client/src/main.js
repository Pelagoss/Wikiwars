import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import './assets/style/tailwind.scss'
import './utils/vee-validate'
import App from './App.vue'
import {$axios} from "./utils/axios"
import router from "./router";

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)

const app = createApp(App);

app.config.globalProperties.$axios = { ...$axios }

app.use(pinia);
app.use(router);

app.mount('#app');
