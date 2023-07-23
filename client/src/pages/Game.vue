<template>
    <div class="grid grid-cols-12 h-[100vh] relative overflow-hidden bgTable">
        <div ref="frame" class="frame" :class="{'opened': game?.is_started === true}"></div>
        <link rel="stylesheet" href="/wiki.css"/>

        <div ref="door_un" class="door col-span-12 flex flex-col items-center justify-end h-full gap-6 text-white z-30"
             :class="{'opened': game?.is_started === true}">
            <div class="font-medium text-4xl mb-8 z-10">
                <div>
                    Début : {{ game?.start?.replaceAll('_', ' ') }}
                </div>
                <div>
                    Fin : {{ game?.target?.replaceAll('_', ' ') }}
                </div>
            </div>

            <div class="w-56 h-56 z-10">
                <Loader></Loader>
            </div>

            <div class="z-10 -mb-20">
                En attente du lancement de la partie...
            </div>
        </div>

        <div ref="door_deux" class="door col-span-12 flex flex-col items-center justify-start h-full gap-6 text-white z-30"
            :class="{'opened': game?.is_started === true}">
            <div class="text-light text-center font-bold my-3 flex justify-center items-center z-10 pt-24">
                {{ game?.users?.length }} joueur(s)
                <icone-dynamique-composant icon="User" class="ml-3 w-5 h-5"></icone-dynamique-composant>
            </div>

            <Button v-if="game?.host === id && game?.is_started === false && loadPage === false && socketJoined === true"
                    class="btnv-success z-10"
                    @click="launch"
            >
                Start !
            </Button>
        </div>

        <leaderboard :game="game" @hover-link="hoverLink" @unhover-link="unhoverLink"/>

        <div ref="wiki" class="m-4 ml-8 col-start-4 col-span-9 game" v-show="game?.is_started === true">
            <div v-if="loading === false"
                 class="mw-content-ltr sitedir-ltr ltr mw-body-content parsoid-body mediawiki mw-parser-output grid-col heightGame"
                 :class="{'overflow-hidden h-[100vh]': game?.is_started === false}"
                 v-html="contenu">
            </div>

            <div v-else class="flex flex-col items-center justify-center h-full gap-6">
                <div class="w-56 h-56">
                    <Loader></Loader>
                </div>
                Chargement...
            </div>
        </div>

        <div v-if="game !== null && game?.winner !== null" class="modal-mask">
            <div class="flex flex-col gap-8 justify-center items-center modal-container">
                <Generique v-if="game != null" :start="game?.winner !== null" :game="game" @close="closeGame"/>
            </div>
        </div>

        <transition>
            <div ref="tooltip" class="mwe-popups mwe-popups-type-page mwe-popups-fade-in-up mwe-popups-no-image-pointer mwe-popups-is-not-tall absolute p-3"
                 style="display: none;height:fit-content;z-index:4000"
                 v-show="showTooltip"
                 :class="{'block': showTooltip, 'flipped-x-y': flipxy, 'flipped-x': flipx, 'flipped-y': flipy}"
                 v-html="tooltipContent"
            >
            </div>
        </transition>
    </div>
</template>

<script>
import {toRaw} from "vue";
import {userStore} from "@/store/index.js";
import {socket, state} from '@/utils/socket.js'
import {mapState} from "pinia";
import Button from "@/components/ui/Button.vue";
import IconeDynamiqueComposant from "@/components/IconeDynamiqueComposant.vue";
import Generique from "@/components/Generique.vue";
import Loader from "@/components/ui/Loader.vue";
import Leaderboard from "@/pages/Leaderboard.vue";

export default {
    name: "Game",
    components: {Leaderboard, Loader, Generique, IconeDynamiqueComposant, Button},
    data() {
        return {
            id: '',
            showTooltip: false,
            tooltipContent: '',
            initStarted: false,
            socketJoined: false,
            timeoutHover: null,
            contenu: '',
            loading: true,
            loadPage: true,
            game: {},
            flipxy: false,
            flipx: false,
            flipy: false
        }
    },
    computed: {
        ...mapState(userStore, {isAuthenticated: "isAuthenticated", username: "username"}),
    },
    mounted() {
        this.$refs.wiki.addEventListener("click", this.clickLink.bind(this), false);
        // this.$refs.wiki.addEventListener("mouseenter", this.hoverLink.bind(this), {passive: false, capture: true});
        // this.$refs.wiki.addEventListener("mouseleave", this.unhoverLink.bind(this), {passive: false, capture: true});

        this.fetchGames().then(() => {
            window.addEventListener("keydown",function (e) {
                if (e.keyCode === 114 || (e.ctrlKey && e.keyCode === 70)) {
                    e.preventDefault();
                    console.log("Timeout 5s");
                }
            })

            let games = toRaw(userStore().games);
            let filtered_games = games.filter(g => g.winner == null);
            this.game = filtered_games[0]

            if (this.game == null) {
                this.$router.push({name: 'accueil'});
            } else {
                if (this.isAuthenticated === true) {
                    this.id = userStore().id;
                    this.initSocket();
                }

                this.fetchPage(this.game.clics[userStore().username].page);
            }
        });
    },
    methods: {
        closeGame() {
            this.destroy();

            this.$nextTick(() => {
                this.$router.push({name: 'accueil'});
            });
        },
        fetchGames() {
            return new Promise((resolve) => {
                this.loadPage = true;
                this.$axios.get('/games').then(({data}) => {
                    this.games = data.reverse();
                    userStore().games = this.games.filter(g => g.users.map(u => u.username).includes(userStore().username));
                }).finally(() => {
                    this.loadPage = false;
                    resolve();
                });
            })
        },
        initSocket() {
            if (this.initStarted || Object.keys(this.game).length === 0) {
                return;
            }

            this.initStarted = true;

            socket.emit('join', this.game);
            this.socketJoined = true;
            this.initStarted = false;

            this.error = false;

            socket.on("PAGE_CHANGED", (data) => {
                this.game = data;
            });

            socket.on("GAME_FINISHED", (data) => {
                this.game = data;
            });

            socket.on('START_GAME', (data) => {
                this.game = data;

                this.$nextTick(() => {
                    this.$refs.wiki.querySelectorAll('a').forEach((a) => {
                //         a.addEventListener("click", this.clickLink.bind(this), false);
                        a.addEventListener("mouseenter", this.hoverLink.bind(this), false);
                        a.addEventListener("mouseleave", this.unhoverLink.bind(this), false);
                    });
                });
            });

            socket.on('connect_error', (e) => {
                this.error = true;
            });

            this.initStarted = false;
        },
        destroy() {
            socket.emit('leave', this.game);

            socket.off("connect");
            socket.off("PAGE_CHANGED");
            socket.off("GAME_FINISHED");
            socket.off("START_GAME");
        },
        launch() {
            this.$refs.door_un.classList.add('opened');
            this.$refs.door_deux.classList.add('opened');
            this.$refs.frame.classList.add('opened');

            this.$axios.post('/game/launch').finally(() => {
                this.loading = false;
            });
        },
        clickLink(event) {
            if (event.target.tagName.toLowerCase() === 'a') {
                event.preventDefault();

                this.showTooltip = false;

                this.fetchPage(event.target['data-title']);
            }
        },
        hoverLink(event) {
            if (event.target.tagName.toLowerCase() === 'a') {
                event.target["data-title"] = event.target.title;
                event.target.title = '';

                event.preventDefault();
                this.timeoutHover = setTimeout(() => {
                    this.fetchLink(event);
                }, 250);
            }
        },
        unhoverLink(event) {
            if (event.target.tagName.toLowerCase() === 'a') {
                event.preventDefault();
                clearTimeout(this.timeoutHover);
                this.toggleTooltip(false, event);
            }
        },
        fetchPage(title) {
            this.loading = true;
            return this.$axios.get('/game/page/' + title).then(({data}) => {
                this.contenu = data.replace(/<\/body>/, '').replace(/<body["'=\w0-9a-zA-Z-,_ ]*>/, '');
            }).finally(() => {
                this.loading = false;
                //
                if (this.game?.is_started === true) {
                    this.$nextTick(() => {
                        this.showTooltip = false;

                        this.$refs.wiki.querySelectorAll('a').forEach((a) => {
                //             a.addEventListener("click", this.clickLink.bind(this), false);
                            a.addEventListener("mouseenter", this.hoverLink.bind(this), false);
                            a.addEventListener("mouseleave", this.unhoverLink.bind(this), false);
                        });
                    });
                }
            });
        },
        fetchLink(event) {
            if (event.target["data-title"] != null) {
                this.$axios.get('/game/link/' + event.target["data-title"]).then(({data}) => {
                    if (data.extract_html != null && data.extract_html !== '') {
                        this.toggleTooltip(true, event);
                        this.tooltipContent = '<div class="mwe-popups-container"><span class="mwe-popups-extract" dir="ltr" lang="fr">'+ data.extract_html +'</span></div>';
                    }
                }).finally(() => {
                    this.loading = false;
                });
            }
        },
        toggleTooltip(val, event) {
            if (val === true) {
                let depasseY = (250 + (event.target.getBoundingClientRect().y + event.target.offsetHeight)) > window.innerHeight;
                let depasseX = (350 + event.target.getBoundingClientRect().x) > window.innerWidth;
                let top;
                let bottom;
                let left;
                let right;

                if (depasseY && depasseX) {
                    this.flipxy = true;
                    this.flipx = false;
                    this.flipy = false;

                    top = `auto`;
                    bottom = `${window.innerHeight - event.target.getBoundingClientRect().y + (event.target.offsetHeight / 2)}px`;
                    right = `${window.innerWidth - (event.target.getBoundingClientRect().x + 20)}px`;
                    left = `auto`;

                } else if (depasseY) {this.flipxy = false;
                    this.flipx = false;
                    this.flipy = true;

                    top = `auto`;
                    bottom = `${window.innerHeight - event.target.getBoundingClientRect().y + (event.target.offsetHeight / 2)}px`;
                    right = `auto`;
                    left = `${event.target.getBoundingClientRect().x}px`;
                } else if (depasseX) {
                    this.flipxy = false;
                    this.flipx = true;
                    this.flipy = false;

                    top = `${event.target.getBoundingClientRect().y + event.target.offsetHeight + (event.target.offsetHeight / 3)}px`;
                    bottom = `auto`;
                    right = `${window.innerWidth - (event.target.getBoundingClientRect().x + 20)}px`;
                    left = `auto`;
                } else {
                    this.flipxy = false;
                    this.flipx = false;
                    this.flipy = false;

                    top = `${event.target.getBoundingClientRect().y + event.target.offsetHeight + (event.target.offsetHeight / 3)}px`;
                    bottom = `auto`;
                    right = `auto`;
                    left = `${event.target.getBoundingClientRect().x}px`;
                }

                this.$refs.tooltip.style.top = top;
                this.$refs.tooltip.style.bottom = bottom;
                this.$refs.tooltip.style.left = left;
                this.$refs.tooltip.style.right = right;

                this.showTooltip = true;
            } else {
                this.showTooltip = false;

                if (event !== null && event?.target["data-title"] != null) {
                    event.target.title = event.target["data-title"];
                }
            }
        }
    },
    watch: {
        isAuthenticated: {
            handler() {
                if (this.isAuthenticated !== false) {
                    this.initSocket();
                }

            },
            immediate: true
        },
        id() {
            if (this.id === null) {
                this.$router.push({'name': 'acceuil'})
            }
        }
    },
    destroyed() {
        this.destroy();
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

    width: 100vw;
    height: 100vh;
}

.game {
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.80);
    backdrop-filter: blur(10px);
    position: absolute;
    height: calc(100vh - 2rem);
    width: calc(100% - 3rem);
}

.heightGame {
    height: calc(100vh - 2rem);
}

.bgTable {
    background: url("/images/table_bg.gif") no-repeat center !important;
    background-size: cover !important;
}

.frame {
    position: fixed;
    width: 100%;
    height: 100%;

    background: #101215;

    z-index: 50;
    clip-path: polygon(0% 0%, 0% 100%, 20% 90%, 10% 80%, 10% 25%, 25% 10%, 75% 10%, 90% 25%, 90% 80%, 80% 90%, 20% 90%, 0% 100%, 100% 100%, 100% 0%);
    transition: cubic-bezier(.29,.01,.47,-0.1) 1s;
    transition-delay: 1.25s;

    &:after {
        content: "";
        position: absolute;

        background-color: #666666;
        background-image: url("https://www.transparenttextures.com/patterns/redox-01.png");

        clip-path: polygon(0% 0%, 0% 100%, 19% 91%, 9.5% 81%, 9.5% 24%, 24% 9.5%, 76% 9.5%, 90.5% 24%, 90.5% 81%, 81% 91%, 19% 91%, 0% 100%, 100% 100%, 100% 0%);

        width: 100%;
        height: 100%;
    }

    &.opened {
        scale: 1.6;
    }
}

.door {
    transition: cubic-bezier(.74,.19,.23,.75) 2s;
    transform: translateY(0);
    opacity: 100%;
    width: 100%;
    height: 50vh;
    position: relative;

    & > * {
        transition: ease-in-out 2s !important;
    }

    &:nth-of-type(2) {
        &:before, &:after {
            content: "";
            width: 100%;
            position: absolute;
            clip-path: polygon(0 0, 100% 0, 100% 85%, 80% 85%, 78% 80%, 70% 80%, 60% 100%, 40% 100%, 30% 80%, 22% 80%, 20% 85%, 0 85%);
            top: 0;
        }

        &:before {
            height: 121.5%;
            background-color: #2F2F2FFF;
        }

        &:after {
            height: 120.5%;
            background-color: #6b6b6b;
            background-image: url("https://www.transparenttextures.com/patterns/low-contrast-linen.png");
            background-size: 20%;
        }
    }


    &:nth-of-type(3) {
        &:before, &:after {
            content: "";
            width: 100%;
            position: absolute;
            clip-path: polygon(20% 20%, 22% 15%, 30% 15%, 40% 35%, 60% 35%, 70% 15%, 78% 15%, 80% 20%, 100% 20%, 100% 100%, 0 100%, 0 20%);
            bottom: 0;
        }

        &:before {
             height: 121.5%;
             background-color: #2F2F2FFF;
        }

        &:after {
            height: 120.5%;
            background-color: #6b6b6b;
            background-image: url("https://www.transparenttextures.com/patterns/low-contrast-linen.png");
            background-size: 15%;
        }
    }

    &.opened {
        &:nth-of-type(2) {
            transform: translateY(-122%);

            & > * {
                opacity: 0%;
            }
        }

        &:nth-of-type(3) {
            transform: translateY(122%);

            & > * {
                opacity: 0%;
            }
        }
    }
}

</style>