<template>
    <Modal @close="$emit('close')" persistent :closable="true" class-modal="h-fit min-h-1/2 w-1/3" v-model="show">
        <div v-if="loading === false">
            <Profile :user="user" friend-view/>
        </div>

        <div v-else class="text-white h-full flex items-center min-h-[50vh]">
            <saber-loader class="self-center grow"/>
        </div>
    </Modal>
</template>

<script>
import SaberLoader from "@/components/ui/SaberLoader.vue";
import Modal from "@/components/ui/Modal.vue";
import Profile from "@/components/MainMenu/Profile.vue";

export default {
    name: "FriendModal",
    components: {Profile, Modal, SaberLoader},
    props: {
        showModalFriend: {
            type: Boolean
        },
        friend: {
            type: [null, Object]
        }
    },
    data() {
        return {
            loading: true,
            show: false,
            user: null
        };
    },
    created() {
        this.$axios.post('/users', {username: this.friend.username}).then(({data}) => {
            this.user = data;
            this.loading = false;
        });
    },
    watch: {
        showModalFriend: {
            handler() {
                this.show = this.showModalFriend;
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