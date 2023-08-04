<template>
    <div class="w-full grid grid-cols-12 h-2/3">
        <div class="flex flex-col col-span-full h-full border border-gray-400 border-opacity-50 text-white">
            <div class="uppercase font-squadaOne text-2xl title">
                <div class="px-8 pt-20 pb-20">Social</div>
                <div class="menu">
                    <div @click="tabToShow = 'amis'"
                         :class="{'active': tabToShow === 'amis'}">
                        Vos amis
                    </div>

                    <div @click="tabToShow = 'invitations'"
                         :class="{'active': tabToShow === 'invitations'}">
                        Invitations d'amis
                    </div>
                </div>
            </div>

            <div
                v-if="loading === false"
                id="TabGames"
                class="grow">
                <table v-if="tabToShow === 'amis'" class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <tbody>
                        <tr v-if="friends.length !== 0">
                            <td colspan="2" class="w-full">
                                <div class="overflow-y-auto scroll-light h-full">
                                    <table>
                                        <tbody>
                                            <tr v-for="(friend, index) in amis">
                                                <td class="w-6/12">
                                                    {{ friend.username }}
                                                </td>
                                                <td class="w-6/12">
                                                    {{ friend.status === 'pending' ? 'Demande envoyée...' : {true: 'En ligne', false: 'Hors ligne'}[friend.isOnline] }}
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <table v-else-if="tabToShow === 'invitations'" class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <tbody>
                    <tr v-if="friends_invitation.length !== 0">
                        <td colspan="2" class="w-full">
                            <div class="overflow-y-auto scroll-light h-full">
                                <table>
                                    <tbody>
                                    <tr v-for="(friend, index) in invitations">
                                        <td class="w-6/12 font-squadaOne text-xl">
                                            {{ friend.username }}
                                        </td>
                                        <td class="w-6/12">
                                            <div class="flex gap-4 justify-center">
                                                <Button class="btnv-success">Accepter</Button>
                                                <Button class="btnv-4">Refuser</Button>
                                            </div>
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
    data() {
        return {
            friends: [],
            friends_invitation: [],
            loading: true,
            tabToShow: 'amis'
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
        ...mapState(userStore, {'user': "getUser"}),
        amis() {
            let friends = this.friends.filter(f => f.status === 'friends').sort((a, b) => a.username.localeCompare(b.username));
            friends = [...friends, ...this.friends.filter(f => f.status === 'pending').sort((a, b) => a.username.localeCompare(b.username))];
            return friends;
        }
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
    background-position-y: 65%;
    @apply relative;
}

.menu {
    @apply flex absolute bottom-0 text-base w-full;

    & div {
        @apply ease-out duration-300 w-full text-gray-400 flex items-center justify-center py-2 border border-b-0 border-l border-r-0 border-gray-400 uppercase font-squadaOne cursor-pointer;
        background-color: rgba(190, 190, 190, 0.15);
        backdrop-filter: blur(20px);

        &:hover {
            background-color: rgba(255, 255, 255, 0.20);
        }

        &.active {
            @apply text-white border-x border-x-white;
            background-color: rgba(255, 255, 255, 0.25);

            & + div:not(:last-child) {
                @apply border-0;
            }
        }

        &:last-child {
            @apply border-r;
        }
    }
}
</style>