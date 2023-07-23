import {defineStore} from "pinia";
import {isValidJwt, emitter} from '@/utils'
import {$axios} from "@/utils/axios.js";

export const userStore = defineStore('user', {
    state: () => ({
        id: null,
        username: null,
        games: null,
        wins: null,
        jwt: null
    }),
    getters: {
        getUser: (state) => state,
        isAuthenticated: (state) => isValidJwt(state.jwt),
    },
    actions: {
        login(data) {
            return $axios.post('/login', data).then(({data}) => {
                this.id = data.id;
                this.username = data.username;
                this.games = data.games;
                this.wins = data.wins;
                this.jwt = data.jwt;
                localStorage.setItem('token', this.jwt);
            });
        },
        register(data) {
            return $axios.post('/register', data);
        },
        logout() {
            this.id = null;
            this.username = null;
            this.games = null;
            this.wins = null;
            this.jwt = null;
        }
    },
    persist: {
        storage: sessionStorage,
    },
});

export const gameStore = defineStore('game', {
    state: () => ({}),
    getters: {
        getGame: (state) => state,
    },
    actions: {
        createGame() {
            return $axios.post('/game/create')
                .then(({data}) => {
                    this.id = data.id;
                    this.host = data.host;
                    this.is_started = data.is_started;
                    this.start = data.start;
                    this.target = data.target;
                    this.winner = data.winner;
                    this.clics = data.clics;
                });
        },
        joinGame(payload) {
            return $axios.post('/game/join', payload);
        }
    }
})