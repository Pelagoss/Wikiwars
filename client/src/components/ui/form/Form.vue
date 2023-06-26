<template>
    <div>
        <slot name="fields" :formError="error"></slot>

        <div v-if="error !== null" class="w-full flex gap-6 justify-center">
            <div class="w-1/2 text-error text-xs">
                {{ error.message }}
            </div>
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