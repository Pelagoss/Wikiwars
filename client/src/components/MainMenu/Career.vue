<template>
    <div class="w-full grid grid-cols-12 h-2/5">
        <div class="flex flex-col col-span-4 h-full border border-gray-400 border-opacity-50 p-8 bg">
            <div class="title uppercase">Statistiques</div>

            <div class="flex flex-col">
                <div v-for="stat in stats" class="stat">
                    <div>
                        {{ stat.label }}
                        <div v-if="stat?.dont" class="text-xs normal-case">
                            {{ stat.dont?.label }}
                        </div>
                    </div>

                    <div class="text-end">
                        {{ stat.value }}
                        <div v-if="stat?.dont" class="text-xs normal-case text-end">
                            {{ stat.dont?.value }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Profile show-title class="border border-gray-400 border-opacity-50 bg" @toggle-modal-avatar="showModalAvatar = $event" :user="user"/>

        <avatar-modal :show-modal-avatar="showModalAvatar" @close="showModalAvatar=false"></avatar-modal>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";
import {toRaw} from "vue";
import {gameStore, userStore} from "@/store/index.js";
import {mapActions, mapState} from "pinia";
import Profile from "@/components/MainMenu/Profile.vue";
import AvatarModal from "@/components/MainMenu/AvatarModal.vue";

export default {
    name: "Career",
    components: {AvatarModal, Profile, IconeDynamiqueComposant, Button},
    emits: ['change-page'],
    data() {
        return {
            showModalAvatar: false
        }
    },
    created() {
        this.$emitter.$on('SOCKET_CONNECTED', () => this.$socket.emit('join', 'lobby'));
        this.refreshUser();
    },
    computed: {
        stats() {
            return userStore().stats;
        },
        ...mapState(userStore, {user: "getUser"}),
    },
    methods: {
        navTo(route) {
            this.$emit('changePage', route);
        },
        ...mapActions(gameStore, {createGame: "createGame", join: "joinGame"}),
        ...mapActions(userStore, {refreshUser: "me"})
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
    background-color: rgba(190, 190, 190, 0.15);
    backdrop-filter: blur(20px);
}
</style>