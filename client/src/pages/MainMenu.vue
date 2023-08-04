<template>
    <div class="h-[100vh] w-[100vw] bgTable">
        <div class="max-w-7xl h-full bg-red py-16 px-16">
            <div class="menu">
                <div v-for="(tab, i) in tabs" @click="tabToShow = tab.slug"
                     :class="{'active': tabToShow === tab.slug}">
                    {{ tab.label }}
                </div>
            </div>

            <Home @change-page="tabToShow = $event" v-if="tabToShow === 'home'"/>
            <Play @change-page="tabToShow = $event" v-if="tabToShow === 'play'"/>
            <Friends @change-page="tabToShow = $event" v-if="tabToShow === 'friends'"/>
            <Career @change-page="tabToShow = $event" v-if="tabToShow === 'career'"/>

            <div @click="logout" class="quit">
                Quit
            </div>
        </div>
    </div>
</template>

<script>
import Home from "@/components/MainMenu/Home.vue";
import Play from "@/components/MainMenu/Play.vue";
import Friends from "@/components/MainMenu/Friends.vue";
import Career from "@/components/MainMenu/Career.vue";
import {mapActions} from "pinia";
import {userStore} from "@/store/index.js";
import {socket} from "@/utils/socket.js";

export default {
    name: "MainMenu",
    components: {Home, Play, Friends, Career},
    data() {
        return {
            tabToShow: 'home'
        }
    },
    computed: {
        tabs() {
            return [
                {
                    label: 'Home',
                    slug: 'home'
                },
                {
                    label: 'Jouer',
                    slug: 'play'
                },
                {
                    label: 'Social',
                    slug: 'friends'
                },
                {
                    label: 'Profil',
                    slug: 'career'
                },
            ]
        }
    },
    methods: {
        ...mapActions(userStore, {logout: 'logout', user: 'getUser'})
    }
}
</script>

<style lang="scss" scoped>
.quit {
    @apply mt-16 text-gray-400 w-16 flex items-center justify-center py-1 rounded border border-gray-400 border-opacity-50 uppercase font-squadaOne cursor-pointer;
    background-color: rgba(190, 190, 190, 0.15);
    backdrop-filter: blur(20px);

    &:hover {
        @apply text-white;
        background-color: rgba(255, 255, 255, 0.15);
    }

}

.menu {
    @apply flex mb-12;

    & div {
        @apply ease-out duration-300 w-36 text-gray-400 flex items-center justify-center py-2 border border-y-0 border-l border-r-0 border-gray-400 uppercase font-squadaOne cursor-pointer;
        background-color: rgba(190, 190, 190, 0.15);
        backdrop-filter: blur(20px);

        &:hover {
            background-color: rgba(255, 255, 255, 0.15);
        }

        &.active {
            @apply text-white border-x border-white;
            background-color: rgba(255, 255, 255, 0.20);

            & + div:not(:last-child) {
                @apply border-0;
            }
        }

        &:last-child {
            @apply border-r;
        }
    }
}
</style>