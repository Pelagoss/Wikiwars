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
                        <span :class="{'newInvitations': friends_invitations.length > 0}">
                            Invitations d'amis
                        </span>
                    </div>

                    <div @click="tabToShow = 'recherche'"
                         :class="{'active': tabToShow === 'recherche'}">
                            Rechercher des amis
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
                                            <tr v-for="(friend, index) in amis" class="cursor-pointer" @click="openModalFriend(friend)">
                                                <td class="w-6/12 inline-flex items-center gap-3 font-squadaOne text-xl">
                                                    <div class="w-2/12 rounded-lg border-2"
                                                         :class="{true: 'border-accent', false: 'border-error'}[friend.isOnline]">
                                                        <img class="rounded h-auto w-full aspect-square object-cover cursor-pointer" :src="friend.avatar.path">
                                                    </div>
                                                    {{ friend.username }}
                                                </td>

                                                <td class="w-6/12" v-if="friend.status === 'pending'">
                                                    Demande d'ami en attente...
                                                </td>

                                                <td class="w-6/12" v-else>
                                                    <div class="flex gap-3 items-center">
                                                        <div class="h-3 w-3 rounded-full border" :class="[{true: 'bg-accent', false: 'bg-error'}[friend.isOnline]]"></div>

                                                        {{ {true: 'En ligne', false: 'Hors ligne'}[friend.isOnline] }}
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>

                        <tr v-else>
                            <td colspan="2" class="w-full text-center font-squadaOne text-xl">
                                Vous n'avez encore aucun ami
                            </td>
                        </tr>
                    </tbody>
                </table>

                <table v-else-if="tabToShow === 'invitations'" class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <tbody>
                        <tr v-if="friends_invitations.length !== 0">
                            <td colspan="2" class="w-full">
                                <div class="overflow-y-auto scroll-light h-full">
                                    <table>
                                        <tbody>
                                        <tr v-for="(friend, index) in friends_invitations" class="cursor-pointer" @click.prevent.stop="openModalFriend(friend)">
                                            <td class="w-6/12 inline-flex items-center gap-3 font-squadaOne text-xl">
                                                <div class="w-2/12 rounded-lg border-2"
                                                     :class="{true: 'border-accent', false: 'border-error'}[friend.isOnline]">
                                                    <img class="rounded h-auto w-full aspect-square object-cover cursor-pointer" :src="friend.avatar.path">
                                                </div>
                                                {{ friend.username }}
                                            </td>

                                            <td class="w-6/12">
                                                <div class="flex gap-4 justify-center">
                                                    <Button class="btnv-success" @click.prevent.stop="manage(true, friend)">Accepter</Button>
                                                    <Button class="btnv-4" @click.prevent.stop="manage(false, friend)">Refuser</Button>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>

                        <tr v-else>
                            <td colspan="2" class="w-full text-center font-squadaOne text-xl">
                                Vous n'avez aucune demande d'amis
                            </td>
                        </tr>
                    </tbody>
                </table>

                <table v-else-if="tabToShow === 'recherche'" class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <tbody>
                        <tr class="h-12">
                            <td>
                                <div class="p-3">
                                    <text-field
                                        label="Rechercher un utilisateur"
                                        @update:model-value="fetchUsers"
                                        class="flex flex-col gap-2"
                                        v-model="search"/>
                                </div>
                            </td>
                        </tr>
                        <tr v-if="users.length !== 0">
                            <td colspan="2" class="w-full">
                                <div class="overflow-y-auto scroll-light h-full">
                                    <table>
                                        <tbody>
                                        <tr v-for="(friend, index) in users" class="cursor-pointer">
                                            <td class="w-6/12 inline-flex items-center gap-3 font-squadaOne text-xl">
                                                <div class="w-2/12 rounded-lg border-2"
                                                     :class="{true: 'border-accent', false: 'border-error'}[friend.isOnline]">
                                                    <img class="rounded h-auto w-full aspect-square object-cover cursor-pointer" :src="friend.avatar.path">
                                                </div>
                                                {{ friend.username }}
                                            </td>

                                            <td class="w-6/12">
                                                <div class="flex gap-4 justify-center">
                                                    <Button class="btnv-success" @click="openModalFriend(friend)">Voir le profil</Button>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>

                        <tr v-else>
                            <td v-if="loadingSearch === false" colspan="2" class="w-full text-center font-squadaOne text-xl">
                                {{ search === null || search === '' ? "Entrez le nom d'un utilisateur pour rechercher" : "Aucun joueur trouvé" }}
                            </td>

                            <td v-else>
                                <saber-loader class="self-center grow"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <saber-loader v-else class="self-center grow"/>
        </div>

        <friend-modal v-if="friendClicked !== null" :show-modal-friend="showModalFriend" :friend="friendClicked" @close="showModalFriend=false; friendClicked = null;"></friend-modal>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import {friendsStore, gameStore, userStore} from "@/store/index.js";
import {mapActions, mapState} from "pinia";
import SaberLoader from "@/components/ui/SaberLoader.vue";
import FriendModal from "@/components/MainMenu/FriendModal.vue";
import TextField from "@/components/ui/form/TextField.vue";
import {useRoute} from "vue-router";

export default {
    name: "Friends",
    components: {TextField, FriendModal, SaberLoader, Button},
    data() {
        return {
            loading: true,
            loadingSearch: false,
            showModalFriend: false,
            friendClicked: null,
            tabToShow: 'amis',
            users: [],
            searchUsersTimeout: null,
            search: null
        };
    },
    created() {
        this.fetchFriends().finally(() => this.loading = false);
        this.$emitter.$on('SOCKET_CONNECTED', () => this.$socket.emit('join', 'lobby'));

        if (this.$socketState.connected) {
            this.$socket.emit('join', 'lobby');
        }
    },
    computed: {
        ...mapState(userStore, {'user': "getUser"}),
        ...mapState(friendsStore, {'friends': "getFriends", "friends_invitations": "getFriendsInvitations"}),
        amis() {
            let friends = this.friends.filter(f => f.status === 'friends').sort((a, b) => a.username.localeCompare(b.username));
            friends = [...friends, ...this.friends.filter(f => f.status === 'pending').sort((a, b) => a.username.localeCompare(b.username))];
            return friends;
        }
    },
    methods: {
        ...mapActions(friendsStore, {'fetchFriends': "fetchFriends", "manageInvitation": "manageInvitation"}),
        manage(response, friend) {
            return this.manageInvitation(response, friend).then(() => {
                this.tabToShow = 'amis';
            }).finally(() => this.loading = false);
        },
        openModalFriend(friend) {
            this.showModalFriend = true;
            this.friendClicked = friend;
        },
        fetchUsers(value) {
            if (this.searchUsersTimeout != null) {
                clearTimeout(this.searchUsersTimeout);
            }

            if (value.value == null || value.value.length < 2) {
                return;
            }

            this.searchUsersTimeout = setTimeout(() => {
                this.loadingSearch = true;
                console.log(value.value);
                if (value.value != null) {
                    this.$axios.post('/users-search', {username: value.value}).then(({data}) => {
                        this.users = data;
                    }).catch((e) => {
                        console.error(e);
                    }).finally(() => {
                        this.loadingSearch = false;
                    });
                }
            }, 400);
        },
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