<template>
    <Modal @close="$emit('close')" persistent :closable="true" height="50%" width="30%" v-model="show">
        <div v-if="loading === false">
            <div>
                <!-- todo: show different avatar to choose the one for profile -->
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

export default {
    name: "AvatarModal",
    components: {Modal, SaberLoader},
    props: {
        showModalAvatar: {
            type: Boolean
        }
    },
    data() {
        return {
            loading: true,
            show: false
        };
    },
    created() {
        this.loading = false;
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