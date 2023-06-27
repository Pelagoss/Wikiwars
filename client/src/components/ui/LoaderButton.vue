<template>
    <div class="loader" :style="{ width }" :class="{'loader-circular': !linear}">
        <svg class="circular" viewBox="25 25 50 50" :style="{ stroke: color }" v-if="!linear">
            <circle class="path" cx="50" cy="50" r="20" fill="none" stroke-width="2" stroke-miterlimit="10"/>
        </svg>

        <div class="linear" v-else>
            <div class="linear-bar"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LoaderButton",
    props: {
        width: {
            type: String,
            default: "25px"
        },
        color: {
            type: String,
            default: "lightgrey"
        },
        linear: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<style scoped lang="scss">
.loader {
    position: relative;
    margin: 0 auto;

    &.loader-circular {
        &:before {
            content: '';
            display: block;
            padding-top: 100%;
        }
    }
}

.circular {
    animation: rotate 2s linear infinite;
    height: 100%;
    transform-origin: center center;
    width: 100%;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
}

.path {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
    animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
    stroke-linecap: round;
}

.linear {
    height: 2px;
    position: relative;
    overflow: hidden;
    background: linear-gradient(103deg, #0997C1 2%, #3E1696 100%);

    .linear-bar {
        position: absolute;
        width: calc(100% * 2/7);
        height: 100%;
        display: flex;
        animation: indeterminate-bar 2s linear infinite;
        background-color: white;
    }
}

@keyframes indeterminate-bar
{
    0%   {transform: translate(-100%, 0)}
    100% {transform: translate(calc(7/2*100%), 0)}
}

</style>
