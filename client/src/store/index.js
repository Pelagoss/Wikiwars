import {defineStore} from "pinia";
import axios from "axios";

export const userStore = defineStore('user', {
    state: () => ({
        username: null,
        wins: null,
        loses: null,
        ratio: null
    }),
    getters: {
        getUser: (state) => state,
        isAuthenticated: (state) => state.username !== null,
    },
    actions: {
        login(data) {
            return axios.post('/login', data).then(({data}) => {
                this.username = data.username;
                this.wins = data.wins;
                this.loses = data.loses;
                this.ratio = data.ratio;
            });
        },
        logout(state) {
            return axios.post('/logout').then(() => {
                this.username = null;
                this.wins = null;
                this.loses = null;
                this.ratio = null;
            });
        }
    },
    persist: {
        storage: sessionStorage, // data in sessionStorage is cleared when the page session ends.
    },
});