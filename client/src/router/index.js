import Game from "../pages/Game.vue";
import {createRouter, createWebHistory} from "vue-router"
import Accueil from "../pages/Accueil.vue";
import Inscription from "../pages/Inscription.vue";

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
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;