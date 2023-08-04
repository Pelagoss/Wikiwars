<template>
    <div class="w-full grid grid-cols-12 h-2/3">
        <div class="flex flex-col col-span-full h-full border border-gray-400 border-opacity-50 text-white">
            <div class="px-8 py-20 uppercase font-squadaOne text-2xl title">
                Rejoignez une partie
            </div>

            <div
                v-if="loading === false"
                @click="joinGame(isInGame)"
                id="TabGames"
                class="grow">
                <table class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <thead v-if="partieEnCours.length !== 0">
                    <tr>
                        <!-- <th class="text-left">#</th>-->
                        <!-- <th class="text-left">Host</th>-->
                        <th class="w-2/12">Joueurs</th>
                        <th class="w-1/3">Départ</th>
                        <th class="w-1/3">Arrivée</th>
                        <th class="w-full"></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-if="partieEnCours.length !== 0">
                        <td colspan="6" class="w-full">
                            <div class="overflow-y-auto scroll-light h-full">
                                <table>
                                    <tbody>
                                    <tr v-for="(game, index) in partieEnCours">
                                        <!-- <td>-->
                                        <!--     {{ index }}-->
                                        <!-- </td>-->
                                        <!--                        <td>-->
                                        <!--                            {{ game.host }}-->
                                        <!--                        </td>-->
                                        <td class="w-2/12">
                                            {{ game.users.length }}
                                        </td>
                                        <td class="w-1/3">
                                            {{ game.start.replaceAll('_', ' ') }}
                                        </td>
                                        <td class="w-1/3">
                                            {{ game.target.replaceAll('_', ' ') }}
                                        </td>
                                        <td class="flex justify-center w-full">
                                            <Button v-if="game.is_started === false" class="btnv-success" @click="joinGame(game.id)">
                                                Rejoindre
                                            </Button>
                                            <Button v-else-if="game.is_started === true && game.winner === null" class="bg-yellow-700">
                                                Partie en cours...
                                            </Button>
                                            <Button v-else-if="game.is_started === true && game.winner !== null" class="bg-red-700">
                                                Partie terminée
                                            </Button>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="6" class="text-center">
                            <div v-if="isInGame !== null"
                            class="flex flex-col gap-8 items-center">
                                <h1 class="sm:text-3xl text-lg">Vous avez une partie en cours, rejoignez la !</h1>
                                <Button class="btnv-success" @click="joinGame(isInGame)">Rejoindre !</Button>
                            </div>
                            <h1 v-else
                                class="sm:text-3xl text-lg">
                                Aucune partie n'est encore créée !
                            </h1>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <saber-loader v-else class="self-center grow"/>
        </div>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import {toRaw} from "vue";
import {gameStore, userStore} from "@/store/index.js";
import {mapActions} from "pinia";
import {emitter} from "@/utils/index.js";
import {socket, state} from "@/utils/socket.js";
import SaberLoader from "@/components/ui/SaberLoader.vue";

export default {
    name: "Play",
    components: {SaberLoader, Button},
    emits: ['change-page'],
    data() {
        return {
            games: [],
            loading: true
        };
    },
    created() {
        this.fetchGames();
        emitter.$on('SOCKET_CONNECTED', () => socket.emit('join', 'lobby'));

        if (state.connected) {
            socket.emit('join', 'lobby');
            socket.on('NEW_GAME', (data) => this.addGame(data));
            socket.on('GAME_STARTED', (data) => this.updateGame(data));
            socket.on('FINISH_GAME', (data) => this.removeGame(data));
        }
    },
    computed: {
        partieEnCours() {
            if (this.isInGame !== null) {
                return [];
            }

            return this.games.filter(
                g => g.winner === null && !g.users.map(u => u.username).includes(userStore().username)
            ).sort(
                (a, b) => a.is_started - b.is_started
            );
        },
        isInGame() {
            let games = toRaw(userStore().games);
            let filtered_games = games.filter(g => g.winner === null);

            return filtered_games.length === 0 ? null : filtered_games[0].id;
        }
    },
    methods: {
        addGame(data) {
            this.games.push(data);
        },
        updateGame(data) {
            let game = this.games.find(g => g.id === data.id);
            game.is_started = data.is_started;
        },
        removeGame(data) {
            this.games = this.games.filter(g => g.id !== data.id);
        },
        handleGames(data) {
            this.games = data.reverse();
            userStore().games = this.games.filter(g => g.users.map(u => u.username).includes(userStore().username));
            userStore().wins = this.games.filter(g => g.winner?.id === userStore().id);
        },
        fetchGames() {
            return this.$axios.get('/games').then(({data}) => {
                this.handleGames(data);
            }).finally(() => this.loading = false);
        },
        navTo(route) {
            this.$emit('changePage', route);
        },
        joinGame(game_id = null) {
            if (game_id !== null) {
                this.join({id: game_id}).then(() => {
                    this.$router.push({name: 'game'});
                })
            }
        },
        ...mapActions(gameStore, {createGame: "createGame", join: "joinGame"})
    }
}
</script>

<style lang="scss" scoped>
.title {
    background: url(/images/cene.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    background-position-y: 60%;
}
</style>