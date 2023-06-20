<template>
    <div>
        <label :for="name" class="text-base">{{ label }}</label>

        <div class="input-form">
            <input v-model="content" :name="name" required="required" :id="name" :type="type">
        </div>

        <div v-if="helpText" :id="name+'help'" class="text-xs text-grey0">{{ helpText }}</div>
    </div>
</template>
<script>
export default {
    name: 'TextField',
    props: {
        name: {
            type: String,
            default: 'field'
        },
        modelValue: {},
        helpText: {
            type: String,
            default: null
        },
        label: {
            type: String,
            default: ''
        },
        type: {
            type: String,
            default: 'text'
        }
    },
    data() {
        return {
            content: this.modelValue
        }
    },
    watch: {
        content: {
            handler() {
                this.$emit('update:modelValue', this.content);
            }
        }
    }
}
</script>

<style lang="scss" scoped>
@import '../../../assets/style/style';
</style>