import {defineStore} from "pinia";
import {isValidJwt} from '@/utils'
import $axios from "@/utils/axios.js";
import {socket} from "@/utils/socket.js";

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
        isAuthenticated: (state) => {

            if (state.id !== null) {
                socket.auth = {id: state.id }
                socket.connect();
            }

            return isValidJwt(state.jwt)
        },
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

                socket.auth = {id: this.id }
                socket.connect();
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
            socket.disconnect();
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

export const friendsStore = defineStore('friends', {
    state: () => ({
        friends: [],
        friends_invitations: []
    }),
    getters: {
        getFriends: (state) => state.friends,
        getFriendsInvitations: (state) => state.friends_invitations,
    },
    actions: {
        handleFriends(data) {
            this.friends = data.filter(f => f.status !== 'pending' || userStore()?.getUser.id === f.user_id);
            this.friends_invitations = data.filter(f => f.status === 'pending' && userStore()?.getUser.id !== f.user_id);
        },
        fetchFriends() {
            return $axios.get('/friends').then(({data}) => {
                this.handleFriends(data);
            });
        },
        manageInvitation(response, friend) {
            return $axios.post('/friends', {user_id: friend.user_id, accept: response}).then(({data}) => {
                this.handleFriends(data);
            });
        }
    }
})