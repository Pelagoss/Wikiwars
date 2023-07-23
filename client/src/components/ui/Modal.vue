<template>
    <div>
        <div class="fixed bottom-0 right-0 top-0 left-0 z-[99999]" v-if="modelValue" @wheel="scroll" @touchmove="scroll" @scroll="scroll">
            <div class="bg-black/70 h-full w-full" v-if="overlay" @click="clickOutside"></div>

            <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 max-h-full glassmorphism" :style="{width: width}">
                <div v-if="closable" class="absolute top-2 right-2 cursor-pointer" @click="$emit('close');$emit('update:modelValue', false)">
                    <IconeDynamiqueComposant :style="{color: crossColor}" class="w-5 h-5" icon="XMark"/>
                </div>

                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";

export default {
    name: "Modal",
    components: {IconeDynamiqueComposant},
    emits: ["update:modelValue", 'close'],
    props: {
        modelValue: {},
        overlay: {
            type: Boolean,
            default: true,
            required: false
        },
        width: {
            type: String,
            default: "25vw",
            required: false
        },
        closable: {
            type: Boolean,
            default: true,
            required: false
        },
        persistent: {
            type: Boolean,
            default: false
        },
        crossColor: {
            type: String,
            default: "white",
            required: false,
        },
        disableScroll: {
            type: Boolean,
            default: false,
            required: false,
        }
    },
    methods: {
        scroll(event) {
            if(this.disableScroll){
                event.preventDefault()
            }
        },
        clickOutside() {
            if (this.persistent === false) {
                this.$emit('close');
                this.$emit('update:modelValue', false);
            }
        }
    }
}
</script>

<style scoped lang="scss">

.glassmorphism {
    @apply rounded;

    border: 1px solid rgba(255, 255, 255, 0.18);
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
}

</style>
