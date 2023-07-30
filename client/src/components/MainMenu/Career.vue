<template>
    <div class="w-full grid grid-cols-12 h-2/5 bg">
        <div class="flex flex-col col-span-4 h-full border border-gray-400 border-opacity-50 p-8">
            <div class="title uppercase">Statistiques</div>

            <div class="flex flex-col">
                <div v-for="stat in stats" class="stat">
                    <div>
                        {{ stat.label }}
                    </div>

                    <div>
                        {{ stat.value }}
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-col col-span-6 h-full border border-gray-400 border-opacity-50 p-8">
            <div class="title uppercase">Profil</div>
            <!-- TODO Mettre une photo de profil -->
            <img class="h-32 w-32 rounded-full self-center" src="https://i.pinimg.com/564x/8d/ff/c8/8dffc810ac2226282085257e73a60761.jpg"/>

            <div class="title self-center pt-6">{{ username }}</div>
        </div>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";
import {toRaw} from "vue";
import {gameStore, userStore} from "@/store/index.js";
import {mapActions, mapState} from "pinia";
import {emitter} from "@/utils/index.js";
import {socket, state} from "@/utils/socket.js";

export default {
    name: "Career",
    components: {IconeDynamiqueComposant, Button},
    emits: ['change-page'],
    created() {
        emitter.$on('SOCKET_CONNECTED', () => socket.emit('join', 'lobby'));
    },
    computed: {
        stats() {
            return [
                {label: 'Victoires', value: this.wins},
                {label: 'Parties jouées', value: this.games},
                {label: 'Ratio V/D', value: this.ratio},
            ]
        },
        wins() {
            return toRaw(userStore().wins).length;
        },
        loses() {
            return toRaw(userStore().games).length - this.wins;
        },
        games() {
            return toRaw(userStore().games).length;
        },
        ratio() {
            return this.wins / (this.loses === 0 ? 1.00 : this.loses);
        },
        ...mapState(userStore, {username: "username"}),
    },
    methods: {
        navTo(route) {
            this.$emit('changePage', route);
        },
        ...mapActions(gameStore, {createGame: "createGame", join: "joinGame"})
    }
}
</script>

<style lang="scss" scoped>
.title {
    @apply text-2xl font-squadaOne text-white pb-6;
}

.stat {
    @apply border border-gray-400 flex justify-between text-white px-4 py-2 uppercase;
}

.bg {
    & > div {
        background-color: rgba(190, 190, 190, 0.15);
        backdrop-filter: blur(20px);
    }
}
</style>