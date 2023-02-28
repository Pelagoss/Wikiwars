<template>
    <div class="w-full h-full sm:grid sm:grid-cols-12 bg-[#101010] flex flex-col">
        <div class="relative col-span-6 flex flex-col items-center sm:h-full w-full h-1/2 bgWiki">
            <form method="post" class="absolute bottom-0 sm:mb-8 mb-3">
                <Button class="btnv-success" icon="Play">
                    Start Game
                </Button>
            </form>
        </div>
        <div class="sm:h-full w-full h-1/2 flex flex-col col-span-6">
            <div class="h-1/2 pt-6" id="TabGames">
                <table>
                    <thead>
                    <tr>
                        <th class="text-left">#</th>
                        <th class="text-left">Host</th>
                        <th class="text-left">Joueurs</th>
                        <th class="text-left">Départ</th>
                        <th class="text-left">Arrivée</th>
                        <th class="text-left w-1/6"></th>
                    </tr>
                    </thead>
                    <tbody class="table-hover">
                    <tr v-if="games.length !== 0" v-for="(game, index) in games">
                        <td>
                            {{ index }}
                        </td>
                        <td>
                            {{ game.host }}
                        </td>
                        <td>
                            {{ game.players.length }}
                        </td>
                        <td>
                            {{ game.start_page.replaceAll('_', ' ') }}
                        </td>
                        <td>
                            {{ game.target_page.replaceAll('_', ' ') }}
                        </td>
                        <button v-if="game.started === false" class="bg-green-500">
                            Rejoindre
                        </button>
                        <button v-else-if="game.started === true && game.winner === false" class="bg-red-700">
                            Partie en cours...
                        </button>
                        <button v-else-if="game.started === true && game.winner === false" class="bg-red-700">
                            Partie terminée
                        </button>
                    </tr>
                    <tr v-else>
                        <td colspan="6" class="text-center bgTable">
                            <h1 class="sm:text-3xl text-lg">
                                Aucune partie n'est encore créée !
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
                            <div class="font-medium sm:text-xl text-xs">{{ user.wins }}</div>
                        </div>
                    </div>
                    <div class="bg-red-500 rounded sm:grid grid-cols-12 gap-6 mb-6 sm:p-6 p-3 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 sm:h-full w-full" icon="Trophy" type="outline"/>
                        <div class="col-span-6 flex flex-col gap-1 sm:text-right">
                            <h3 class="font-bold sm:text-xl text-xs">Défaites</h3>
                            <div class="font-medium sm:text-xl text-xs">{{ user.loses }}</div>
                        </div>
                    </div>
                    <div class="bg-yellow-500 rounded sm:grid grid-cols-12 gap-6 mb-6 sm:p-6 p-3 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 sm:h-full w-full" icon="ChartPie" type="solid"/>
                        <div class="col-span-6 flex flex-col gap-1 sm:text-right">
                            <h3 class="font-bold sm:text-xl text-xs">Ratio V/D</h3>
                            <div class="font-medium sm:text-xl text-xs">{{ user.ratio }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Button from "./ui/Button.vue";
import IconeDynamiqueComposant from "./IconeDynamiqueComposant.vue";
import {mapState} from "pinia";
import {userStore} from "../store/index.js";

export default {
    name: "Lobby",
    components: {IconeDynamiqueComposant, Button},
    data() {
        return {
            games: []
        };
    },
    computed: {
        ...mapState(userStore,{user: "getUser"})
    },
    created() {
        // axios.get('/listGames').then(({data}) => {
        //     this.games = data.games.reverse();
        // })
    }
}
</script>

<style scoped>
.bgWiki {
    background: url("/WikiWarsGif.gif") no-repeat center;
    background-size: cover;
}

.bgTable {
    background: url("/table_bg.gif") no-repeat center;
    background-size: cover;
}
</style>