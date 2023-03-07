<template>
    <div class="grid grid-cols-12">
        <link rel="stylesheet" href="/wiki.css"/>

        <div class="col-span-3 flex flex-col m-6 relative">
            <div class="leaderboard">
                <h1 class="flex flex-col">
                    <div class="flex gap-6 items-center">
                        <icone-dynamique-composant icon="Trophy" class="w-12 h-12"></icone-dynamique-composant>
                        <div class="text-2xl">
                            Statistiques
                        </div>
                    </div>
                    <div class="grid text-white pt-3 grid-cols-3 font-bold">
                        <div>Joueur</div>
                        <div>Page actuelle</div>
                        <div># Clics</div>

                    </div>
                </h1>
                <ol>
                    <li v-for="(player, index) in game.users">
                        <div class="grid text-white px-4 py-3 grid-cols-3">
                            <div>{{ player.username }}</div>
                            <div>{{ game.clics[player.username].page }}</div>
                            <div>{{ game.clics[player.username].clics }}</div>

                        </div>
                    </li>
                </ol>
            </div>
        </div>

        <div v-if="!loading" ref="wiki"
             class="mw-content-ltr sitedir-ltr ltr mw-body-content parsoid-body mediawiki mw-parser-output overflow-x-hidden col-start-4 col-span-9 grid-col"
             :class="{'overflow-hidden h-[100vh]': game.is_started === false}"
             v-html="contenu">

        </div>

        <div v-if="game.is_started === false || loading === true || game.winner !== null" class="modal-mask">
            <div class="flex flex-col gap-8 justify-center items-center modal-container">
                <div class="scale-[2]">
                    <slot name="header" v-if="game.winner === null">
                        <div class="lds-default w-32 h-32"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
                    </slot>
                </div>

                <div class="modal-body">
                    <slot v-if="game.is_started === false" name="body">
                        En attente du lancement de la partie...

                        <div class="text-light text-center font-bold my-3 flex justify-center items-center">
                            {{ game.users.length }} joueur(s)
                            <icone-dynamique-composant icon="User" class="ml-3 w-5 h-5"></icone-dynamique-composant>
                        </div>
                    </slot>

                    <slot v-else-if="game != null && game?.winner !== null" name="body">
                        <Generique :start="game != null && game?.winner !== null" :game="game"/>
                    </slot>

                    <slot v-else name="body">
                        Chargement...
                    </slot>
                </div>

                <div v-if="game.host === id && game.is_started === false" class="modal-footer">
                    <slot name="footer">
                        <Button
                            class="btnv-success"
                            @click="launch"
                        >
                            Start !
                        </Button>
                    </slot>
                </div>
                <div v-else-if="game.winner !== null" class="modal-footer">
                    <slot name="footer">
                        <Button
                            class="btnv-4"
                            @click="$router.push({name: 'accueil'})"
                        >
                            Quitter
                        </Button>
                    </slot>
                </div>
            </div>
        </div>

        <transition>
            <div ref="tooltip" class="mwe-popups mwe-popups-type-page mwe-popups-fade-in-up mwe-popups-no-image-pointer mwe-popups-is-not-tall absolute p-3"
                 aria-hidden="" style="display: block;height:fit-content;z-index:4000"
                 v-show="showTooltip"
                 v-html="tooltipContent"
            >
            </div>
        </transition>
    </div>
</template>

<script>
import {toRaw} from "vue";
import {userStore} from "../store/index.js";
import socket from '../utils/socket.js'
import {mapState} from "pinia";
import Button from "../components/ui/Button.vue";
import IconeDynamiqueComposant from "../components/IconeDynamiqueComposant.vue";
import router from "../router/index.js";
import Generique from "../components/Generique.vue";

export default {
    name: "Game",
    components: {Generique, IconeDynamiqueComposant, Button},
    data() {
        return {
            id: '',
            showTooltip: false,
            title: '',
            tooltipContent: '',
            initStarted: false,
            socket: null,
            contenu: '',
            loading: true,
            game: {}
        }
    },
    computed: {
        ...mapState(userStore, {isAuthenticated: "isAuthenticated", username: "username"}),
    },
    mounted() {
        let games = toRaw(userStore().games);
        let filtered_games = games.filter(g => g.winner == null);
        this.game = filtered_games[0]

        if (this.isAuthenticated === true) {
            this.id = userStore().id;
            this.initSocket();
        }

        this.fetchPage(this.game.clics[userStore().username].page);
    },
    created() {
        this.fetchGames();
    },
    methods: {
        fetchGames() {
            this.$axios.get('/games').then(({data}) => {
                this.games = data.reverse();
                userStore().games = this.games.filter(g => g.users.map(u => u.username).includes(userStore().username));
            })
        },
        initSocket() {
            if (this.initStarted) {
                return;
            }

            this.initStarted = true;

            socket.connect();

            socket.on("connect", () => {
                socket.emit('join', this.game)
            })

            socket.on("session", ({token}) => {
                this.loading = false;
                this.initStarted = false;

                this.error = false;
            });

            socket.on("PAGE_CHANGED", (data) => {
                this.game = data;
            });

            socket.on("GAME_FINISHED", (data) => {
                this.game = data;
            });

            socket.on('START_GAME', (data) => {
                console.log("Game started");
                this.game = data;
            });

            socket.on('connect_error', (e) => {
                this.error = true;
            });
        },
        launch() {
            this.$axios.post('/game/launch').finally(() => {
                this.loading = false;
            });
        },
        clickLink(event) {
            event.preventDefault();

            this.fetchPage(event.target.title);
        },
        hoverLink(event) {
            event.preventDefault();

            this.fetchLink(event);
        },
        unhoverLink(event) {
            event.preventDefault();

            this.toggleTooltip(false, event)
        },
        fetchPage(title) {
            this.loading = true;
            this.$axios.get('/game/page/' + title).then(({data}) => {
                this.contenu = data.replace(/<\/body>/, '').replace(/<body["'=\w0-9a-zA-Z-,_ ]*>/, '');
            }).finally(() => {
                this.loading = false;
            });
        },
        fetchLink(event) {
            this.$axios.get('/game/link/' + event.target.title).then(({data}) => {
                this.toggleTooltip(true, event)
                this.tooltipContent = '<div class="mwe-popups-container"><span class="mwe-popups-extract" dir="ltr" lang="fr">'+ data.extract_html +'</span></div>';
            }).finally(() => {
                this.loading = false;
            });
        },
        toggleTooltip(val, event) {
            if (val === true) {
                this.title = event.target.title;
                event.target.title = '';
                console.log(event);
                this.$refs.tooltip.style.top = `${event.pageY + event.target.offsetHeight}px`;
                this.$refs.tooltip.style.left = `${event.target.offsetLeft + (event.target.offsetWidth/2)}px`;
                this.showTooltip = true;
            } else {
                this.showTooltip = false;
                event.target.title = this.title;
            }
        }
    },
    watch: {
        token: {
            handler() {
                if (this.isAuthenticated !== false) {
                    this.initSocket();
                }

            },
            immediate: true
        },
        loading() {
            if (this.loading === false) {
                this.$nextTick(() => {
                    this.$refs.wiki.querySelectorAll('a').forEach((a) => {
                        a.addEventListener("click", this.clickLink.bind(this), false);
                        a.addEventListener("mouseenter", this.hoverLink.bind(this), false);
                        a.addEventListener("mouseleave", this.unhoverLink.bind(this), false);
                    });
                })
            }
        },
        id() {
            if (this.id === null) {
                this.$router.push({'name': 'acceuil'})
            }
        }
    },
    destroyed() {
        socket.disconnect();

        socket.off("session");
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

.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    display: flex;
    transition: opacity 0.3s ease;
}

.modal-container {
    margin: auto;
    border-radius: 2px;
    transition: all 0.3s ease;
}

.lds-default {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
}
.lds-default div {
    position: absolute;
    width: 6px;
    height: 6px;
    background: #fff;
    border-radius: 50%;
    animation: lds-default 1.2s linear infinite;
}
.lds-default div:nth-child(1) {
    animation-delay: 0s;
    top: 37px;
    left: 66px;
}
.lds-default div:nth-child(2) {
    animation-delay: -0.1s;
    top: 22px;
    left: 62px;
}
.lds-default div:nth-child(3) {
    animation-delay: -0.2s;
    top: 11px;
    left: 52px;
}
.lds-default div:nth-child(4) {
    animation-delay: -0.3s;
    top: 7px;
    left: 37px;
}
.lds-default div:nth-child(5) {
    animation-delay: -0.4s;
    top: 11px;
    left: 22px;
}
.lds-default div:nth-child(6) {
    animation-delay: -0.5s;
    top: 22px;
    left: 11px;
}
.lds-default div:nth-child(7) {
    animation-delay: -0.6s;
    top: 37px;
    left: 7px;
}
.lds-default div:nth-child(8) {
    animation-delay: -0.7s;
    top: 52px;
    left: 11px;
}
.lds-default div:nth-child(9) {
    animation-delay: -0.8s;
    top: 62px;
    left: 22px;
}
.lds-default div:nth-child(10) {
    animation-delay: -0.9s;
    top: 66px;
    left: 37px;
}
.lds-default div:nth-child(11) {
    animation-delay: -1s;
    top: 62px;
    left: 52px;
}
.lds-default div:nth-child(12) {
    animation-delay: -1.1s;
    top: 52px;
    left: 62px;
}
@keyframes lds-default {
    0%, 20%, 80%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.5);
    }
}

/*--------------------
Body
--------------------*/
*,
*::before,
*::after {
    box-sizing: border-box;
}

body {
    min-height: 450px;
    height: 100vh;
    margin: 0;
    background: radial-gradient(ellipse farthest-corner at center top, #f39264 0%, #f2606f 100%);
    color: #fff;
    font-family: "Open Sans", sans-serif;
}

/*--------------------
Leaderboard
--------------------*/
.leaderboard {
    position: absolute;
    width: 100%;
    height: max-content;
    background: linear-gradient(to bottom, #3a404d, #181c26);
    border-radius: 10px;
    box-shadow: 0 7px 30px rgba(62, 9, 11, 0.3);
}

.leaderboard h1 {
    font-size: 18px;
    color: #e1e1e1;
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