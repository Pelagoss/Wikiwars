<template>
    <transition name='fade'>
        <aside
            class="toast"
        >
            <slot>
                {{ data?.message }} {{ data?.i }}
                {{ data?.data.username }}
            </slot>
        </aside>
    </transition>
</template>
<script>
export default {
    props: {
        data: {
            type: Object
        }
    },
    mounted() {
        if(this.data.timeout) {
            window.setTimeout(() => {
                this.$parent.deleteToast(this.data.i);
            }, this.data.timeout);
        }
    }
}
</script>

<style lang="scss" scoped>
.toast {
    border-radius: 0.25rem;
    padding: 1rem 0.75rem;
    width: 100%;
    color: white;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>