<template>
    <Icon />
</template>

<script>
import { defineAsyncComponent } from 'vue'
export default {
    name: "IconeDynamiqueComposant",
    props: {
        type: {
            type: String|null,
            required: true,
            default: null
        }
    },
    components: {
        Icon: defineAsyncComponent(() =>
            import(`./icons/${this.type}.vue`)
        )
    }
}
</script>

<style scoped>

</style>
