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
            <div class="h-1/2 pt-6" id="TabGames">
                <table :class="{'h-full':  partieEnCours.length === 0}">
                    <thead>
                    <tr>
                        <th class="text-left">#</th>
                        <!--                        <th class="text-left">Host</th>-->
                        <th class="text-left">Joueurs</th>
                        <th class="text-left">Départ</th>
                        <th class="text-left">Arrivée</th>
                        <th class="text-left w-1/6"></th>
                    </tr>
                    </thead>
                    <tbody class="table-hover">
                    <tr v-if="partieEnCours.length !== 0" v-for="(game, index) in games">
                        <td>
                            {{ index }}
                        </td>
                        <!--                        <td>-->
                        <!--                            {{ game.host }}-->
                        <!--                        </td>-->
                        <td>
                            {{ game.users.length }}
                        </td>
                        <td>
                            {{ game.start.replaceAll('_', ' ') }}
                        </td>
                        <td>
                            {{ game.target.replaceAll('_', ' ') }}
                        </td>
                        <td class="flex justify-center w-full">
                            <Button v-if="game.is_started === false" class="btnv-success" @click="joinGame(game.id)">
                                Rejoindre
                            </Button>
                            <Button v-else-if="game.is_started === true && game.winner === false" class="bg-yellow-700">
                                Partie en cours...
                            </Button>
                            <Button v-else-if="game.is_started === true && game.winner === true" class="bg-red-700">
                                Partie terminée
                            </Button>
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
import Button from "../components/ui/Button.vue";
import IconeDynamiqueComposant from "../components/IconeDynamiqueComposant.vue";
import {mapActions, mapState} from "pinia";
import {gameStore, userStore} from "../store/index.js";
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
            return this.games.filter(g => g.winner === null && !g.users.map(u => u.username).includes(userStore().username));
        },
        isInGame() {
            let games = toRaw(userStore().games);
            let filtered_games = games.filter(g => g.winner === null);

            return filtered_games.length === 0 ? null : filtered_games[0].id;
        }
    },
    created() {
        this.fetchGames();
    },
    methods: {
        fetchGames() {
            return this.$axios.get('/games').then(({data}) => {
                this.games = data.reverse();
                userStore().games = this.games.filter(g => g.users.map(u => u.username).includes(userStore().username));
                userStore().wins = this.games.filter(g => g.winner?.id === userStore().id);
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
@import '../assets/style/style.scss';
</style>