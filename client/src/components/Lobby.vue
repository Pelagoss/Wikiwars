<template>
    <div class="w-full h-full grid grid-cols-12">
        <div class="col-span-6">
            <img src="/WikiWarsGif.gif" class="w-[90%] h-[90%]">
            <form method="post" style="position: relative;top: -11vh;left: 17vw;">
                <button style="display:contents;"><a type="submit" class="btnv btnv-3" style="">Start Game<i
                    class="bi bi-play-fill"></i></a></button>
            </form>
        </div>
        <div class="col-span-6">
            <div id="TabGames">
                <table class="table-fill">
                    <thead>
                        <tr>
                            <th class="text-left">#</th>
                            <th class="text-left">Host</th>
                            <th class="text-left">Joueurs</th>
                            <th class="text-left">Départ</th>
                            <th class="text-left">Arrivée</th>
                            <th class="text-left w-1/3"></th>
                        </tr>
                    </thead>
                    <tbody class="table-hover">
                        <tr v-for="(game, index) in games">
                            <td>
                                {{index}}
                            </td>
                            <td>
                                {{game.host}}
                            </td>
                            <td>
                                {{game.players.length}}
                            </td>
                            <td>
                                {{game.start_page.replaceAll('_',' ')}}
                            </td>
                            <td>
                                {{game.target_page.replaceAll('_',' ')}}
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
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Lobby",
    data() {
        return {
            games: []
        };
    },
    created() {
        axios.get('/listGames').then(({data}) => {
            this.games = data.games.reverse();
        })
    }
}
</script>

<style scoped>

</style>