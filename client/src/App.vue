<template>
    <router-view>
    </router-view>
</template>


<script>
import {friendsStore, userStore} from "./store/index.js";
import ToastContainer from "@/components/ui/ToastContainer.vue";

export default {
    name: 'App',
    components: {ToastContainer},
    data() {
        return {
            data: {},
            showToast: false
        }
    },
    mounted() {
        this.$emitter.$on('unAuthorized', (data) => {
            userStore().logout();
        });

        this.$emitter.$on('NOTIFICATION', (data) => {
            this.$notifier.addToast(data)
        });
    }
};

</script>

<style lang="scss" scoped>
</style>