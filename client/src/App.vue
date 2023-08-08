<template>
    <router-view>
    </router-view>
</template>


<script>
import {emitter} from "./utils/index.js";
import {userStore} from "./store/index.js";
import ToastContainer from "@/components/ui/ToastContainer.vue";
import {createApp} from "vue";

emitter.$on('unAuthorized', (data) => {
    console.log(userStore);
    userStore().logout();
});

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
        let toast = createApp(ToastContainer);
        let wrapper = document.createElement('div');
        wrapper.className = 'absolute bottom-0 right-0 flex flex-col-reverse'
        let toastr = toast.mount(wrapper);

        if (document.body) {
            document.body.appendChild(wrapper);
        }

        emitter.$on('NOTIFICATION', (data) => {
            toastr.addToast(data)
        });
    }
};

</script>

<style lang="scss" scoped>
</style>