<template>
    <div>
        <label :class="{'!text-accent': focus}" :for="name" class="text-base">{{ label }}</label>

        <div>
            <input class="focus:border-accent" @focusin="focus = true" @focusout="focus = false" v-model="content" :name="name" required="required" :id="name" :type="type">
        </div>

        <div v-if="helpText" :id="name+'help'" class="text-xs text-grey0" :class="{'!text-accent50': focus}">{{ helpText }}</div>
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
            content: this.modelValue,
            focus: false
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

.form {
    & * {
        transition: color cubic-bezier(0,.15,.56,.77) 300ms;
    }
}

input {
    border: 1px solid rgba(255, 255, 255, 0.18);
    @apply px-4 w-full leading-5 h-12 rounded-lg text-primary outline-none bg-transparent;
}
</style>