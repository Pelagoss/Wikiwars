<template>
    <Form ref="form" @submit="emits('submit')">
        <slot name="fields"></slot>

        <div v-if="error !== null" class="w-full flex gap-6 justify-center">
            <div class="w-1/2 text-error text-xs">
                {{ error }}
            </div>
        </div>
    </Form>
</template>

<script setup>
import {Form} from "vee-validate";
const emits = defineEmits(['submit']);

defineProps({
    error: {}
});
</script>

<style scoped>

</style>