<template>
    <div :ref="name">
        <label :class="{'!text-accent': focus, '!text-error': errors.length > 0}" :for="name"
               class="text-base">{{ label }}</label>

        <div>
            <input :class="{'!border-error': errors.length > 0}" class="focus:border-accent"
                   @focusin="focus = true" @focusout="focus = false" @blur="handleChange" v-model="value" :name="name" required="required"
                   :id="name" :type="type">
        </div>

        <div v-if="helpText" :id="name+'help'" class="text-xs text-grey0"
             :class="{'!text-accent50': focus, '!text-error50': errors.length > 0}">{{ errors.length > 0 ? errors[0] : helpText }}
        </div>
    </div>
</template>

<script setup>
import {ref, toRefs, watch} from "vue";
import {useField} from "vee-validate";

const props = defineProps({
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
    },
    rules: {
        type: [String, Object],
        default: ''
    }
});

const {
    value,
    errors,
    handleChange,
    setErrors
} = useField(() => props.name, props.rules,  {
    initialValue: props.modelValue,
    label: props.label
});

const emit = defineEmits(['update:modelValue'])

const focus = ref(false);

watch(value, () => {
    emit('update:modelValue', value);
});

</script>

<style lang="scss" scoped>
@import '../../../assets/style/style';

.form {
    & * {
        transition: color cubic-bezier(0, .15, .56, .77) 300ms;
    }
}

input {
    border: 1px solid rgba(255, 255, 255, 0.18);
    @apply px-4 w-full leading-5 h-12 rounded-lg text-primary outline-none bg-transparent;
}
</style>