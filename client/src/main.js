import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import '@/assets/style/tailwind.scss'
import '@/assets/style/style.scss'
import '@/utils/vee-validate'
import App from '@/App.vue'
import axios from "@/utils/axios"
import {notifier} from "@/utils/notifier"
import {emitter} from "@/utils/index.js"
import router from "@/router";
import {socket, state} from "@/utils/socket";

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)

const app = createApp(App);

app.config.globalProperties.$axios = axios;
app.config.globalProperties.$socket = socket;
app.config.globalProperties.$socketState = state;
app.config.globalProperties.$emitter = emitter;

app.use(pinia);
app.use(notifier);
app.use(router);
app.provide('axios', axios);
app.provide('socket', socket);

app.mount('#app');
