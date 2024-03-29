<template>
    <div class="flex flex-col col-span-6 h-full p-8 text-white font-squadaOne text-2xl">
        <div v-if="showTitle" class="title uppercase">Profil</div>

        <img
            @click="friendView === false ? $emit('toggle-modal-avatar', true) : $event.preventDefault();"
            class="h-32 w-32 rounded-lg self-center border-4 object-cover"
            :class="[{true: 'border-accent', false: 'border-error', undefined: 'border-cyan-500'}[user.isOnline], {'cursor-pointer': friendView === false}]"
            :src="user?.avatar?.path ?? 'basic.jpg'"
        />

        <div class="title self-center pt-4">{{ user.username }}</div>

        <template v-if="friendView === true">
            <template v-if="user.relation !== null">
                <template v-if="user.relation === 'pending' && user.user_id !== userStore()?.getUser.id">
                    <div class="self-center mt-2 p-3 rounded-lg flex flex-col gap-2 text-base text-center border">
                        Demande a être votre ami
                        <div class="flex gap-4 justify-center">
                            <Button class="btnv-success" @click="manage(true, user)">Accepter</Button>
                            <Button class="btnv-4" @click="manage(false, user)">Refuser</Button>
                        </div>
                    </div>
                </template>

                <template v-if="user.relation === 'pending' && user.user_id === userStore()?.getUser?.id">
                    <div class="flex flex-col gap-2 text-base text-center text-gray-400">
                        Demande d'ami en attente...
                    </div>
                </template>

                <template v-if="user.relation === 'friends'">
                    <div class="self-center mt-2 flex gap-2 text-base text-center">
                        <div class="self-center border px-2 py-1 text-sm border-gray-400 rounded-lg flex items-center gap-2">
                            <icone-dynamique-composant icon="Users" class="!w-4 !h-4"></icone-dynamique-composant>
                            Amis
                        </div>

                        <div v-if="user.isJoinable && (isInGame === null || isInGame === user?.gameId)" @click="joinGame(user?.gameId)"
                             class="self-center border px-2 py-1 text-sm text-accent50 border-accent50 rounded-lg flex items-center gap-2 hover:text-accent cursor-pointer hover:border-accent">
                            <icone-dynamique-composant icon="PaperAirplane" class="!w-4 !h-4"></icone-dynamique-composant>
                            Rejoindre
                        </div>
                    </div>
                </template>
            </template>

            <template v-else>
                <div class="self-center mt-2 flex flex-col gap-2 text-base text-center">
                    <div @click="addFriend"
                        class="self-center border px-2 py-1 mt-2 text-sm text-gray-400 border-gray-400 rounded-lg flex items-center gap-2 hover:text-white cursor-pointer hover:border-white">
                        <icone-dynamique-composant icon="UserPlus" class="!w-4 !h-4"></icone-dynamique-composant>
                        Ajouter aux amis
                    </div>
                </div>
            </template>

            <div class="text-lg w-1/2">
                <div class="title uppercase">Statistiques</div>

                <div class="flex flex-col">
                    <div v-for="stat in user.stats" class="stat">
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
        </template>
    </div>
</template>

<script>

import Button from "@/components/ui/Button.vue";
import {mapActions} from "pinia";
import {friendsStore, gameStore, userStore} from "@/store/index.js";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";
import {toRaw} from "vue";

export default {
    name: "Profile",
    components: {IconeDynamiqueComposant, Button},
    emits: ['toggle-modal-avatar'],
    props: {
        user: {
            type: Object
        },
        friendView: {
          type: Boolean,
          default: false
        },
        showTitle: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        userStore,
        ...mapActions(friendsStore, {'fetchFriends': "fetchFriends", "manageInvitation": "manageInvitation"}),
        ...mapActions(gameStore, {'join': "joinGame"}),
        manage(response, friend) {
            return this.manageInvitation(response, friend).then(() => {
                this.user.relation = response ? 'friends' : null;
                this.tabToShow = 'amis';
            }).finally(() => this.loading = false);
        },
        addFriend() {
            this.$axios.post('/friends/add', {'friend_id': this.user.uid}).then(() => {
                this.fetchFriends();
                this.user.relation = 'pending';
                this.user.user_id = userStore()?.getUser?.id;
            });
        },
        joinGame(game_id = null) {
            if (game_id !== null && this.isInGame !== this.user?.gameId) {
                this.join({id: game_id}).then(() => {
                    this.$router.push({name: 'game'});
                })
            } else if (this.isInGame === this.user?.gameId) {
                this.$router.push({name: 'game'});
            }
        }
    },
    computed: {
        isInGame() {
            let games = toRaw(userStore().games);
            let filtered_games = games.filter(g => g.winner === null);

            return filtered_games.length === 0 ? null : filtered_games[0].id;
        }
    }
}
</script>

<style lang="scss" scoped>
.stat {
    @apply border border-gray-400 flex justify-between text-white px-4 py-2 uppercase;
}
</style>