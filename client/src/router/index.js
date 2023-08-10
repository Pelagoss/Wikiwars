import Game from "@/pages/Game.vue";
import {createRouter, createWebHistory} from "vue-router"
import Accueil from "@/pages/Accueil.vue";
import Inscription from "@/pages/Inscription.vue";
import Email from "@/pages/Email.vue";
import Play from "@/components/MainMenu/Play.vue";
import Friends from "@/components/MainMenu/Friends.vue";
import Career from "@/components/MainMenu/Career.vue";
import Home from "@/components/MainMenu/Home.vue";
import MainMenu from "@/pages/MainMenu.vue";

const routes = [
    {
        path: '/',
        name: 'accueil',
        component: Accueil,
        children: [
            {
                path: '',
                name: 'home',
                component: Home
            },
            {
                path: 'play',
                name: 'play',
                component: Play
            },
            {
                path: 'friends',
                name: 'friends',
                component: Friends
            },
            {
                path: 'career',
                name: 'career',
                component: Career
            },
        ]
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