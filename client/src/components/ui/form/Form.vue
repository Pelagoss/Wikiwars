<template>
    <div>
        <slot name="fields"></slot>

        <div v-if="error !== null" class="self-start text-red-400 text-xs" style="display: block">
            {{ error }}
        </div>
    </div>
</template>

<script>
export default {
    name: "Form",
    props: {
        error: {},
        callback: {}
    }
}
</script>

<style scoped>

</style>