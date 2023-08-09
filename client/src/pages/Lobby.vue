<template>
    <div id="lobby" class="w-full h-full sm:grid sm:grid-cols-12 bg-[#101010] flex flex-col">
        <div class="relative col-span-6 flex flex-col items-center sm:h-full w-full h-1/2 bgWiki">
            <div class="absolute bottom-0 sm:mb-8 mb-3">
                <Button class="btnv-success" icon="Play" @click="joinGame(isInGame)">
                    {{ isInGame !== null ? 'Rejoindre la partie' : 'Start Game' }}
                </Button>
            </div>
        </div>
        <div class="sm:h-full w-full h-1/2 flex flex-col col-span-6">
            <div class="h-1/2 mt-6 w-[90%]" id="TabGames">
                <table class="w-full border-spacing-y-1 border-spacing-x-0 h-full">
                    <thead>
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
                            <td colspan="6" class="text-center bgTable">
                                <h1 class="sm:text-3xl text-lg">
                                    {{ isInGame === 1 ? "Vous avez une partie en cours, rejoignez la !" : "Aucune partie n'est encore créée !"}}
                                </h1>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="flex flex-col items-center h-1/2 pt-6 mx-auto w-[90%]">
                <h2 class="sm:pb-6 pb-3 sm:text-3xl text-base">
                    Vos Stats
                </h2>
                <div class="grid grid-cols-12 gap-4 w-full">
                    <div class="bg-green-500 rounded sm:grid grid-cols-12 gap-6 mb-6 sm:p-6 p-3 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 sm:h-full w-full" icon="Trophy" type="solid"/>
                        <div class="col-span-6 flex flex-col gap-1 sm:text-right">
                            <h3 class="font-bold sm:text-xl text-xs">Victoires</h3>
                            <div class="font-medium sm:text-xl text-xs">{{
                                    /*user.wins ??*/
                                    wins
                                }}
                            </div>
                        </div>
                    </div>
                    <div class="bg-red-500 rounded sm:grid grid-cols-12 gap-6 mb-6 sm:p-6 p-3 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 sm:h-full w-full" icon="Trophy" type="outline"/>
                        <div class="col-span-6 flex flex-col gap-1 sm:text-right">
                            <h3 class="font-bold sm:text-xl text-xs">Défaites</h3>
                            <div class="font-medium sm:text-xl text-xs">{{
                                    /*user.loses ??*/
                                    loses
                                }}
                            </div>
                        </div>
                    </div>
                    <div class="bg-yellow-500 rounded sm:grid grid-cols-12 gap-6 mb-6 sm:p-6 p-3 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 sm:h-full w-full" icon="ChartPie" type="solid"/>
                        <div class="col-span-6 flex flex-col gap-1 sm:text-right">
                            <h3 class="font-bold sm:text-xl text-xs">Ratio V/D</h3>
                            <div class="font-medium sm:text-xl text-xs">{{
                                    /*user.ratio ??*/
                                    ratio
                                }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Button from "@/components/ui/Button.vue";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";
import {mapActions, mapState} from "pinia";
import {gameStore, userStore} from "@/store/index.js";
import {toRaw} from "vue";

export default {
    name: "Lobby",
    components: {IconeDynamiqueComposant, Button},
    data() {
        return {
            games: []
        };
    },
    computed: {
        wins() {
            return toRaw(userStore().wins).length;
        },
        loses() {
            return toRaw(userStore().games).length - this.wins;
        },
        ratio() {
            return this.wins / (this.loses === 0 ? 1.00 : this.loses);
        },
        partieEnCours() {
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
    created() {
        this.fetchGames();
        this.$emitter.$on('SOCKET_CONNECTED', () => this.$socket.emit('join', 'lobby'));

        if (this.$socketState.connected) {
            this.$socket.emit('join', 'lobby');
            this.$socket.on('NEW_GAME', (data) => this.addGame(data));
            this.$socket.on('GAME_STARTED', (data) => this.updateGame(data));
            this.$socket.on('FINISH_GAME', (data) => this.removeGame(data));
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
                this.join({id: game_id}).then(() => {
                    this.fetchGames();

                    this.$router.push({name: 'game'});
                })
            }
        },
        ...mapActions(gameStore, {createGame: "createGame", join: "joinGame"})

    }
}
</script>

<style lang="scss" scoped>
</style>