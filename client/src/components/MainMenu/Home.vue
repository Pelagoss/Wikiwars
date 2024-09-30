<template>
    <div class="w-full grid grid-cols-12 h-2/3 mainGrid">
        <div
            @click="joinGame(isInGame)"
            class="col-span-6 border border-r-0 border-gray-400 border-opacity-50 row-span-2 text-2xl p-8 font-squadaOne uppercase text-white play">
            Play now!
        </div>
        <router-link
            :to="{name: 'career'}"
            class="col-span-6 border border-b-0 border-gray-400 border-opacity-50 text-2xl p-8 font-squadaOne uppercase text-white career">
            Profil
        </router-link>
        <router-link
            :to="{name: 'friends'}"
            class="col-span-6 border border-gray-400 border-opacity-50 text-2xl p-8 font-squadaOne uppercase text-white friends">
            <span :class="{'newInvitations': friends_invitations.length > 0}">
                Social
            </span>
        </router-link>
    </div>
</template>

<script>
import {toRaw} from "vue";
import {friendsStore, gameStore, userStore} from "@/store/index.js";
import {mapActions, mapState} from "pinia";

export default {
    name: "Home",
    emits: ['change-page'],
    computed: {
        ...mapState(friendsStore, {"friends_invitations": "getFriendsInvitations"}),
        isInGame() {
            let games = toRaw(userStore().games);
            let filtered_games = games.filter(g => g.winner === null);

            return filtered_games.length === 0 ? null : filtered_games[0].id;
        }
    },
    methods: {
        navTo(route) {
            this.$emit('changePage', route);
        },
        handleGames(data) {
            userStore().games = data.filter(g => g.users.map(u => u.username).includes(userStore().username));
            userStore().wins = data.filter(g => g.winner?.id === userStore().id);
        },
        fetchGames() {
            return this.$axios.get('/games').then(({data}) => {
                this.handleGames(data);
            });
        },
        joinGame(game_id = null) {
            if (this.isInGame === null && game_id === null) {
                this.createGame().then(() => {
                    this.fetchGames().finally(() => {
                        this.$nextTick(() => {
                            this.$router.push({name: 'game'});
                        })
                    });
                })
            } else {
                if (this.isInGame) {
                    this.join({id: game_id}).then(() => {
                        this.$router.push({name: 'game'});
                    })
                } else {
                    this.navTo('play');
                }
            }
        },
        ...mapActions(gameStore, {createGame: "createGame", join: "joinGame"})
    }
}
</script>

<style lang="scss" scoped>
.mainGrid {
    & div, & a {
        @apply cursor-pointer hover:text-[1.875rem] hover:brightness-150 ease-out duration-300;
    }

    .play {
        background: url("/images/WikiWarsGif.gif") no-repeat center;
        background-size: cover;
        //background: url("/images/death_wiki_star.png") no-repeat center;
        //background-size: 50%;
    }

    .friends {
        background: url(/images/players.png);
        background-size: cover;
        background-repeat: no-repeat;
    }

    .career {
        background: url(/images/career.png);
        background-size: cover;
        background-repeat: no-repeat;
    }
}
</style>
