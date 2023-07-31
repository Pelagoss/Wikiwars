<template>
    <div class="flex flex-col justify-center items-center gap-4">
        <img class="loading-saber w-fit h-32" src="/images/loading_saber.png"/>
        <div class="font-squadaOne text-xl">
            Chargement ...
        </div>
    </div>
</template>
<script>
export default {
    name: 'saber-loader'
}
</script>
<style lang="scss" scoped>

.loading-saber {
    animation: loader-saber 1.15s ease-in-out infinite;
}

@keyframes loader-saber {
    0% {
        clip-path: polygon(0 80%, 25% 65%, 50% 80%, 75% 65%, 100% 80%, 100% 100%, 0 100%);
    }
    50% {
        clip-path: polygon(0 0%, 25% 0%, 50% 0%, 75% 0%, 100% 0%, 100% 100%, 0 100%);
    }
}
</style>