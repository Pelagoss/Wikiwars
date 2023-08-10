<template>
    <div class="flex flex-col col-span-6 h-full p-8 text-white font-squadaOne text-2xl">
        <div v-if="showTitle" class="title uppercase">Profil</div>
        <!-- TODO Mettre une photo de profil -->
        <img class="h-32 w-32 rounded-full self-center" src="https://i.pinimg.com/564x/8d/ff/c8/8dffc810ac2226282085257e73a60761.jpg"/>

        <div class="title self-center pt-6">{{ user.username }}</div>
    </div>
</template>

<script>

export default {
    name: "Profile",
    props: {
        user: {
            type: Object
        },
        showTitle: {
            type: Boolean,
            default: false
        }
    },
}
</script>