<template>
    <div class="h-[100vh] w-[100vw] bgTable">
        <div class="max-w-7xl h-full bg-red py-16 px-16">
            <div class="menu">
                <router-link :to="{name: tab.slug}" v-for="(tab, i) in tabs"
                             exact-active-class="active" exact>
                    <span :class="{'newInvitations': friends_invitations.length > 0 && tab.slug === 'friends'}">
                        {{ tab.label }}
                    </span>
                </router-link>
            </div>

            <router-view></router-view>

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
import {mapActions, mapState} from "pinia";
import {friendsStore, userStore} from "@/store/index.js";

export default {
    name: "MainMenu",
    components: {Home, Play, Friends, Career},
    data() {
        return {
            tabToShow: 'home'
        }
    },
    computed: {
        ...mapState(friendsStore, {"friends_invitations": "getFriendsInvitations"}),
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

    & a {
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