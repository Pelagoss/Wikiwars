<template>
<!--    <Lobby v-if="isAuthenticated" />-->
<!--    <Login v-else />-->
    <main-menu/>
<!--    TODO remettre correctement ça-->
</template>

<script>
import Lobby from "@/pages/Lobby.vue";
import MainMenu from "@/pages/MainMenu.vue";
import Login from "@/pages/Login.vue";
import { mapState } from 'pinia'
import {userStore} from "@/store/index.js";

export default {
    name: "Accueil",
    components: {MainMenu, Login, Lobby},
    created() {
        this.fetchGames();
    },
    computed: {
        ...mapState(userStore,{isAuthenticated: "isAuthenticated"})
    },
    methods: {
        handleGames(data) {
            userStore().games = data.filter(g => g.users.map(u => u.username).includes(userStore().username));
            userStore().wins = data.filter(g => g.winner?.id === userStore().id);
        },
        fetchGames() {
            return this.$axios.get('/games').then(({data}) => {
                this.handleGames(data);
            });
        },
    }
}
</script>

<style lang="scss" scoped>
</style>
