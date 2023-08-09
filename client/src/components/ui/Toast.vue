<template>
    <transition name="slide-fade">
        <aside
            v-if="show"
            class="toast"
            @mouseenter="timer?.pause" @mouseleave="timer?.resume"
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
    data() {
        return {
            timer: null,
            show: false
        }
    },
    methods: {
        createTimer: function (callback, delay) {
            var timerId, start, remaining = delay;

            this.pause = function() {
                window.clearTimeout(timerId);
                timerId = null;
                remaining -= Date.now() - start;
            };

            this.resume = function() {
                if (timerId) {
                    return;
                }

                start = Date.now();
                timerId = window.setTimeout(callback, remaining);
            };

            this.resume();
        }
    },
    mounted() {
        this.show = true

        if(this.data.timeout) {
            let parent = this.$parent;

            this.timer = new this.createTimer(() => {
                    this.show = false;
                    window.setTimeout(() => {
                        parent.deleteToast(this.data.i)
                    }, 150);
                }, this.data.timeout
            );
        }
    }
}
</script>

<style lang="scss" scoped>
.toast {
    @apply border rounded text-white px-3 py-4;
    background-color: rgba(190, 190, 190, 0.15);
    backdrop-filter: blur(20px);
    width: 100%;
}

.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translate3d(0, 100%, 0);
    opacity: 0;
}
</style>