<template>
    <div class="flex flex-col col-span-6 h-full p-8 text-white font-squadaOne text-2xl">
        <div v-if="showTitle" class="title uppercase">Profil</div>

        <img
            @click="friendView === false ? $emit('toggle-modal-avatar', true) : $event.preventDefault();"
            class="h-32 w-32 rounded-lg self-center border-4"
            :class="[{true: 'border-accent', false: 'border-error', undefined: 'border-cyan-500'}[user.isOnline], {'cursor-pointer': friendView === false}]"
            src="https://i.pinimg.com/564x/8d/ff/c8/8dffc810ac2226282085257e73a60761.jpg"
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
                    <div class="self-center border px-2 py-1 mt-2 text-sm border-gray-400 rounded-lg flex items-center gap-2">
                        <icone-dynamique-composant icon="Users" class="!w-4 !h-4"></icone-dynamique-composant>
                        Amis
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
        </template>
    </div>
</template>

<script>

import Button from "@/components/ui/Button.vue";
import {mapActions} from "pinia";
import {friendsStore, userStore} from "@/store/index.js";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";

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
        }
    }
}
</script>