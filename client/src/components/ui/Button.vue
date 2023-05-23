<template>
    <button class="flex items-center md:px-4 md:py-3 px-2 py-1 btnv md:text-base !text-xs">
        <slot></slot>
        <IconeDynamiqueComposant v-if="icon !== null" class="ml-3 sm:w-5 sm:h-5 w-3 h-3" :icon="icon"/>
    </button>
</template>

<script>
import IconeDynamiqueComposant from "../IconeDynamiqueComposant.vue";

export default {
    name: "Button",
    components: {IconeDynamiqueComposant},
    props: {
        icon: {
            type: String,
            required: false,
            default: null
        }
    }
}
</script>

<style lang="scss" scoped>
.btnv{
    color: #fff;
    cursor: pointer;
    text-align: center;
    font-size: 1rem;
    font-weight: 400;
    line-height: 3vh;
    position: relative;
    text-decoration: none;
    text-transform: uppercase;
    border-radius: 1vh;
    width: fit-content;
}

.btnv:hover {
    text-decoration: none;
}

.btnv-success {
    background: #1f9051;
    border: 1px solid #0d5f38;
    box-shadow: 0px 2px 0 #0e6d40, 2px 4px 6px #038447;
    font-weight: 900;
    letter-spacing: 1px;
    transition: all 150ms linear;
}

.btnv-success:hover {
    background: #0f6b40;
    border: 1px solid rgba(0, 0, 0, 0.05);
    box-shadow: 1px 1px 2px rgba(255, 255, 255, 0.2);
    text-decoration: none;
    text-shadow: -1px -1px 0 #08482a;
    transition: all 250ms linear;
}

.btnv-4 {
    background: #e3403a;
    border: 1px solid #da251f;
    box-shadow: 0px 2px 0 #d6251f, 2px 4px 6px #e02a24;
    font-weight: 900;
    letter-spacing: 1px;
    transition: all 150ms linear;
}

.btnv-4:hover {
    background: #e02c26;
    border: 1px solid rgba(0, 0, 0, 0.05);
    box-shadow: 1px 1px 2px rgba(255, 255, 255, 0.2);
    color: #ec817d;
    text-decoration: none;
    text-shadow: -1px -1px 0 #c2211c;
    transition: all 250ms linear;
}

.btnv-5 {
    background: #dee2e6;
    border: 1px solid #b1b1b1;
    box-shadow: 0px 2px 0 #bdafaf, 2px 4px 6px #756e6e;
    font-weight: 900;
    letter-spacing: 1px;
    transition: all 150ms linear;
}

.btnv-5:hover {
    background: #d2d2d2;
    border: 1px solid rgba(0, 0, 0, 0.05);
    box-shadow: 1px 1px 2px rgba(255, 255, 255, 0.2);
    color: #aba5a5de;
    text-decoration: none;
    text-shadow: -1px -1px 0 #5d5a5a;
    transition: all 250ms linear;
}
</style>