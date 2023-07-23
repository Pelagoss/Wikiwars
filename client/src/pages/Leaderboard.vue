<template>
    <div class="leaderboard" v-if="game">
        <h1 class="flex flex-col !mb-4 pb-4">
            <div class="flex gap-6 items-center justify-between">
                <div class="flex gap-6 items-center">
                    <icone-dynamique-composant icon="AdjustmentsHorizontal"
                                               class="!w-8 !h-8"></icone-dynamique-composant>

                    <div class="text-2xl">Partie</div>
                </div>

                <div v-if="game?.started_at !== null"
                     class="flex gap-2 text-white pt-3 justify-center items-end leading-5">
                    <div class="flex gap-2 items-end">
                        <icone-dynamique-composant icon="Clock" class="!w-5 !h-5 font-bold"></icone-dynamique-composant>
                        <div class="font-bold">Temps écoulé</div>
                    </div>
                    <div>
                        {{ elapsedTimeToShow }}
                    </div>
                </div>
            </div>
            <div class="w-full grid grid-cols-2 text-white pt-6 justify-around">
                <div class="col-span-1 flex gap-4 items-center max-w-full">
                    <div class="flex gap-2 items-center">
                        <icone-dynamique-composant icon="Home" class="!w-5 !h-5 font-bold"></icone-dynamique-composant>
                        <div class="font-bold">Départ</div>
                    </div>
                    <div :title="game?.start"
                         @mouseenter="$emit('hoverLink', $event)"
                         @mouseleave="$emit('unhoverLink', $event)"
                        class="overflow-hidden whitespace-nowrap overflow-ellipsis">
                        {{ game?.start?.replaceAll('_', ' ') }}
                    </div>
                </div>

                <div class="col-span-1 flex gap-4 items-center justify-end max-w-full">
                    <div class="flex gap-2 items-center">
                        <icone-dynamique-composant icon="MapPin"
                                                   class="!w-5 !h-5 font-bold"></icone-dynamique-composant>
                        <div class="font-bold">Cible</div>
                    </div>
                    <div :title="game?.target"
                         @mouseenter="$emit('hoverLink', $event)"
                         @mouseleave="$emit('unhoverLink', $event)"
                        class="overflow-hidden whitespace-nowrap overflow-ellipsis">
                        {{ game?.target?.replaceAll('_', ' ') }}
                    </div>
                </div>
            </div>
        </h1>
        <h1 class="flex flex-col">
            <div class="flex gap-6 items-center">
                <icone-dynamique-composant icon="Trophy" class="!w-8 !h-8"></icone-dynamique-composant>
                <div class="text-2xl">
                    Statistiques
                </div>
            </div>
            <div class="grid text-white pt-3 grid-cols-10 font-bold gap-4">
                <div class="col-span-3">Joueur</div>
                <div class="col-span-5">Page actuelle</div>
                <div class="col-span-2 text-center"># Clics</div>

            </div>
        </h1>
        <ol>
            <li v-for="(player, index) in game.users">
                <div class="grid text-white px-4 py-3 grid-cols-10 gap-4">
                    <div class="col-span-3">{{ player.username }}</div>
                    <div class="col-span-5 whitespace-nowrap text-ellipsis overflow-hidden"
                         :title="game.clics[player.username].page"
                         @mouseenter="$emit('hoverLink', $event)"
                         @mouseleave="$emit('unhoverLink', $event)">
                        {{ game.clics[player.username].page?.replaceAll('_', ' ') }}
                    </div>
                    <div class="col-span-2 text-center">{{ game.clics[player.username].clics }}</div>
                </div>
            </li>
        </ol>
    </div>
</template>
<script>
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue"
import moment from "moment";

export default {
    name: 'leaderboard',
    components: {IconeDynamiqueComposant},
    props: {
        game: {
            type: Object
        }
    },
    data() {
        return {
            elapsedTime: moment.duration(0)
        }
    },
    created() {
        setInterval(() => {
            this.elapsedTime = this.formatDateToText(this.startedDate);
        }, 1000);
    },
    methods: {
        formatDateToText(str) {
            moment.locale('fr');
            return moment.duration(moment().diff(moment(str).utc(true)));
        },
        zeroPad(nr, base) {
            let len = (String(base).length - String(nr).length) + 1;
            return len > 0 ? new Array(len).join('0') + nr : nr;
        }
    },
    computed: {
        startedDate() {
            return this.game?.started_at;
        },
        elapsedTimeToShow() {
            return (this.elapsedTime.hours() > 0 ? this.elapsedTime.hours() + ':' : '')
                + (this.elapsedTime.minutes() > 0 ? this.zeroPad(this.elapsedTime.minutes(), 10) + ':' : '00:')
                + (this.elapsedTime.seconds() > 0 ? this.zeroPad(this.elapsedTime.seconds(), 10) : '00');
        }
    }
}
</script>
<style lang="scss" scoped>
body {
    color: unset;
    font-family: unset;
    font-size: 16px;
    font-weight: 400;
    text-rendering: optimizeLegibility;
    text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
}


/*--------------------
Leaderboard
--------------------*/
.leaderboard {
    position: fixed;
    width: 25%;
    height: max-content;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    @apply mt-4 ml-4;
}

.leaderboard h1 {
    font-size: 18px;
    color: #FFFFFF;
    margin-bottom: 0;
    @apply px-4;
}

.leaderboard ol {
    margin: 0;
}

.leaderboard ol li {
    position: relative;
    z-index: 1;
}

</style>