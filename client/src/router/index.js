import Game from "@/pages/Game.vue";
import {createRouter, createWebHistory} from "vue-router"
import Accueil from "@/pages/Accueil.vue";
import Inscription from "@/pages/Inscription.vue";
import Email from "@/pages/Email.vue";

const routes = [
    {
        path: '/',
        name: 'accueil',
        component: Accueil
    },
    {
        path: '/game',
        name: 'game',
        component: Game
    },
    {
        path: '/inscription/:token',
        name: 'inscription',
        component: Inscription
    },
    {
        path: '/emails/:token',
        name: 'email',
        component: Email
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;