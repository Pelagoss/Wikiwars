<template>
    <Toast v-for="toast in toasts" :data="toast" :key="toast.i">
    </Toast>
</template>
<script>
import Toast from "@/components/ui/Toast.vue";

export default {
    components: {Toast},
    props: {
        timeout: {
            type: Number,
            default: 2
        }
    },
    data() {
        return {
            toasts: {},
            count: 0
        }
    },
    methods: {
        addToast(data) {
            this.toasts[this.count] = {
                i: this.count,
                timeout: this.timeout * 1000,
                message: "Ceci est un message",
                data: data
            };

            this.count += 1;
        },
        deleteToast(i) {
            delete this.toasts[i];
        }
    }
}
</script>

<style lang="scss" scoped>
</style>