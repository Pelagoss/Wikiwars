<template>
    <button class="flex items-center px-4 py-3 btnv">
        <slot></slot>
        <IconeDynamiqueComposant v-if="icon !== null" class="ml-3 w-5 h-5" :icon="icon"/>
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