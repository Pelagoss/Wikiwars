<template>
    <Lobby v-if="isAuthenticated" />
    <Login v-else />
</template>

<script>
import Lobby from "@/pages/Lobby.vue";
import Login from "@/pages/Login.vue";
import { mapState } from 'pinia'
import {userStore} from "@/store/index.js";

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

<style lang="scss" scoped>
</style>
