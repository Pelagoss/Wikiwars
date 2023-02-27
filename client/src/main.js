import { createApp } from 'vue'
import './style.scss'
import App from './App.vue'
import axios from "axios"

axios.defaults.baseURL = "127.0.0.1:5000/";


createApp(App).mount('#app')
