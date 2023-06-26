<template>
    <Form v-slot="{ errors }">
        <slot name="fields"></slot>

        <div v-if="error !== null" class="w-full flex gap-6 justify-center">
            <div class="w-1/2 text-error text-xs">
                {{ error.message }}
            </div>
        </div>
    </Form>
</template>

<script>
import {Form} from "vee-validate";
export default {
    name: "Form",
    components: {Form},
    props: {
        error: {},
        callback: {}
    }
}
</script>

<style scoped>

</style>