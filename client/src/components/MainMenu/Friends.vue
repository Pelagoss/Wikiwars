<template>
    <div class="w-full grid grid-cols-12 h-2/3">
        <div class="flex flex-col col-span-full h-full border border-gray-400 border-opacity-50 text-white">
            <div class="px-8 py-12 uppercase font-squadaOne text-2xl title">
                Vos amis
            </div>

            <div
                v-if="loading === false"
                id="TabGames"
                class="grow">
                <table class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <thead>
                    <tr>
                        <th class="w-4/12">Joueurs</th>
                        <th class="w-4/12"></th>
                    </tr>
                    </thead>
                    <tbody>
                        <tr v-if="friends.length !== 0">
                            <td colspan="2" class="w-full">
                                <div class="overflow-y-auto scroll-light h-full">
                                    <table>
                                        <tbody>
                                            <tr v-for="(friend, index) in friends">
                                                <td class="w-6/12">
                                                    {{ friend.username }}
                                                </td>
                                                <td class="w-6/12">
                                                    {{ friend.status === 'pending' ? 'Demande envoyée...' : friend.isOnline }}
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <saber-loader v-else class="self-center grow"/>
        </div>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import {toRaw} from "vue";
import {gameStore, userStore} from "@/store/index.js";
import {mapActions, mapState} from "pinia";
import {emitter} from "@/utils/index.js";
import {socket, state} from "@/utils/socket.js";
import SaberLoader from "@/components/ui/SaberLoader.vue";

export default {
    name: "Friends",
    components: {SaberLoader, Button},
    emits: ['change-page'],
    data() {
        return {
            friends: [],
            friends_invitation: [],
            loading: true
        };
    },
    created() {
        this.fetchFriends();
        emitter.$on('SOCKET_CONNECTED', () => socket.emit('join', 'lobby'));

        if (state.connected) {
            socket.emit('join', 'lobby');
        }
    },
    computed: {
        ...mapState(userStore, {'user': "getUser"})
    },
    methods: {
        handleFriends(data) {
            this.friends = data.filter(f => f.status !== 'pending' || this.user.id === f.user_id);
            this.friends_invitation = data.filter(f => f.status === 'pending' && this.user.id !== f.user_id);
        },
        fetchFriends() {
            return this.$axios.get('/friends').then(({data}) => {
                this.handleFriends(data);
            }).finally(() => this.loading = false);
        }
    }
}
</script>

<style lang="scss" scoped>
.title {
    background: url(/images/players.png);
    background-repeat: no-repeat;
    background-size: cover;
    background-position-y: 60%;
}
</style>