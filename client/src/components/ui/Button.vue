<template>
    <button class="flex items-center md:px-4 md:py-3 px-2 py-1 btnv md:text-base !text-xs">
        <slot></slot>
        <IconeDynamiqueComposant v-if="icon !== null" class="ml-3 sm:w-5 sm:h-5 w-3 h-3" :icon="icon"/>
    </button>
</template>

<script>
import IconeDynamiqueComposant from "../IconeDynamiqueComposant.vue";

export default {
    name: "Button",
    components: {IconeDynamiqueComposant},
    props: {
        icon: {
            type: String,
            required: true,
            default: null
        }
    }
}
</script>

<style scoped>

</style>