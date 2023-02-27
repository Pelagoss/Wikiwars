<template>
    <div class="w-full h-full grid grid-cols-12 bg-[#101010]">
        <div class="col-span-6 flex flex-col items-center h-full w-full bgWiki">
            <form method="post" class="absolute bottom-0 mb-8">
                <Button class="btnv-success" icon="Play">
                    Start Game
                </Button>
            </form>
        </div>
        <div class="flex flex-col col-span-6">
            <div class="h-1/2" id="TabGames">
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
                            <h1 class="text-3xl">
                                Aucune partie n'est encore créée !
                            </h1>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div class="flex flex-col items-center h-1/2 pt-6 mx-auto w-[90%]">
                <h2 class="pb-6">
                    Vos Stats
                </h2>
                <div class="grid grid-cols-12 gap-4 w-full">
                    <div class="bg-green-500 rounded grid grid-cols-12 gap-6 mb-6 p-6 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 h-full w-full" icon="Trophy" type="solid"/>
                        <div class="col-span-6 flex flex-col gap-1 text-right">
                            <h3 class="font-bold">Victoires</h3>
                            <div class="font-medium text-xl">{{ user.wins }}</div>
                        </div>
                    </div>
                    <div class="bg-red-500 rounded grid grid-cols-12 gap-6 mb-6 p-6 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 h-full w-full" icon="Trophy" type="outline"/>
                        <div class="col-span-6 flex flex-col gap-1 text-right">
                            <h3 class="font-bold">Défaites</h3>
                            <div class="font-medium text-xl">{{ user.loses }}</div>
                        </div>
                    </div>
                    <div class="bg-yellow-500 rounded grid grid-cols-12 gap-6 mb-6 p-6 col-span-4">
                        <IconeDynamiqueComposant class="col-span-4 h-full w-full" icon="ChartPie" type="solid"/>
                        <div class="col-span-6 flex flex-col gap-1 text-right">
                            <h3 class="font-bold">Ratio V/D</h3>
                            <div class="font-medium text-xl">{{ user.ratio }}</div>
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

export default {
    name: "Lobby",
    components: {IconeDynamiqueComposant, Button},
    data() {
        return {
            games: [],
            user: {username: "Pelagoss", wins: 2, loses: 0, ratio: "100.0 %"}
        };
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
    background: url("/WikiWarsGif.gif");
    background-repeat: no-repeat;
    background-size: cover;
}

.bgTable {
    background: url("/table_bg.gif");
    background-repeat: no-repeat;
    background-size: cover;
}
</style>