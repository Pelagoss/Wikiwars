<template>
    <Lobby v-if="isAuthenticated" />
    <Login v-else />
</template>

<script>
import Lobby from "./Lobby.vue";
import Login from "./Login.vue";
import { mapState } from 'pinia'
import {userStore} from "../store/index.js";

export default {
    name: "Accueil",
    components: {Login, Lobby},
    data() {
        return {
            count: 0
        }
    },
    computed: {
        ...mapState(userStore,{isAuthenticated: "isAuthenticated"})
    }
}
</script>

<style scoped>
</style>
