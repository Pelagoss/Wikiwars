<template>
    <Modal @close="$emit('close')" persistent :closable="true" height="50%" width="30%" v-model="show">
        <div v-if="loading === false" class="p-8 flex flex-col justify-between h-full">
            <div class="grid grid-cols-6 gap-4">
                <div v-for="a in avatars" @click="avatarSelected = a.path">
                    <img class="h-16 w-16 object-cover cursor-pointer rounded-lg border-4 hover:border-accent50 hover:scale-110"
                         :class="[{'!border-accent': avatarSelected === a.path}]"
                         :src="a.path">
                </div>
                <!-- todo: show different avatar to choose the one for profile -->
            </div>
            <div class="flex justify-end">
                <Button class="btnv-success"
                        @click.prevent.stop="console.log(avatarSelected)"
                        :disabled="avatarSelected === user.avatar.path">
                    Sauvegarder
                </Button>
            </div>
        </div>

        <div v-else class="text-white h-full flex items-center">
            <saber-loader class="self-center grow"/>
        </div>
    </Modal>
</template>

<script>
import SaberLoader from "@/components/ui/SaberLoader.vue";
import Modal from "@/components/ui/Modal.vue";
import {mapState} from "pinia";
import {userStore} from "@/store/index.js";
import Button from "@/components/ui/Button.vue";

export default {
    name: "AvatarModal",
    components: {Button, Modal, SaberLoader},
    props: {
        showModalAvatar: {
            type: Boolean
        }
    },
    data() {
        return {
            loading: true,
            avatars: [],
            show: false,
            avatarSelected: '',
        };
    },
    created() {
        this.$axios.get('/avatars').then((r) => {
            this.avatars = r.data;
            this.avatarSelected = this.user?.avatar?.path;
            this.loading = false;
        });
    },
    computed: {
        ...mapState(userStore, {user: "getUser"})
    },
    watch: {
        showModalAvatar: {
            handler() {
                this.show = this.showModalAvatar;
            },
            immediate: true
        }
    }
}
</script>

<style lang="scss" scoped>
.center {
    @apply justify-center items-center;
}
</style>