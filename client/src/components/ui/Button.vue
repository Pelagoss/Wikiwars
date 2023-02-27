<template>
    <button class="rounded-full">
        <slot></slot>
        <IconeDynamiqueComposant v-if="icon !== null" class="ml-3 h-6 w-6" :type="icon"></IconeDynamiqueComposant>
    </button>
</template>

<script>
import IconeDynamiqueComposant from "../IconeDynamiqueComposant.vue";

export default {
    name: "Button",
    components: {IconeDynamiqueComposant},
    props: {
        icon: {
            type: String|null,
            required: true,
            default: null
        }
    }
}
</script>

<style scoped>

</style>