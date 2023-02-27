<template>
    <component class="w-5 h-5" :is="iconComponent"/>
</template>

<script>
import * as solid from "@heroicons/vue/24/solid"
import * as outline from "@heroicons/vue/24/outline"

export default {
    name: "IconeDynamiqueComposant",
    props: {
        icon: {
            type: String,
            required: true,
            default: null
        },
        type: {
            type: String,
            required: false,
            default: 'solid'
        }
    },
    computed: {
        icons() {
            return {solid, outline}
        },
        iconComponent() {
            return this.icons[this.type][this.icon + "Icon"];
        }
    }
}
</script>

<style scoped>

</style>
