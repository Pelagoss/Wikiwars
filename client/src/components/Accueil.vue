<template>
    <Lobby v-if="user !== null">
    </Lobby>
</template>

<script>
import Lobby from "./Lobby.vue";

export default {
    name: "Accueil",
    components: {Lobby},
    data() {
        return {
            count: 0,
            user: {username: "Pelagoss"}
        }
    }
}
</script>

<style scoped>
</style>
