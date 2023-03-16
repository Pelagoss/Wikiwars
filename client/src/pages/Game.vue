<template>
    <div class="grid grid-cols-12 h-[100vh] relative overflow-hidden bgTable">
        <div ref="frame" class="frame"></div>
        <link rel="stylesheet" href="/wiki.css"/>

        <div ref="door_un" class="door col-span-12 flex flex-col items-center justify-end h-full gap-6 text-white z-30" v-if="game?.is_started === false">
            <div class="font-medium text-4xl mb-12 z-10">
                <div>
                    Début : {{ game?.start?.replaceAll('_', ' ') }}
                </div>
                <div>
                    Fin : {{ game?.target?.replaceAll('_', ' ') }}
                </div>
            </div>

            <div class="scale-[2] z-10">
                <Loader></Loader>
            </div>

            <div class="z-10 -mb-20">
                En attente du lancement de la partie...
            </div>
        </div>

        <div ref="door_deux" class="door col-span-12 flex flex-col items-center justify-start h-full gap-6 text-white z-30" v-if="game?.is_started === false">
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

        <div class="leaderboard">
            <h1 class="flex flex-col !mb-8">
                <div class="flex gap-6 items-center">
                    <icone-dynamique-composant icon="AdjustmentsHorizontal" class="!w-8 !h-8"></icone-dynamique-composant>
                    <div class="text-2xl">
                        Partie
                    </div>
                </div>
                <div class="grid text-[#101010] pt-3 grid-cols-10 gap-4">
                    <div class="font-bold col-span-3">Départ</div>
                    <div class="col-span-7" :title="game?.start"
                         @mouseenter="hoverLink"
                         @mouseleave="unhoverLink">
                        {{ game?.start?.replaceAll('_', ' ') }}
                    </div>
                </div>
                <div class="grid text-[#101010] pt-3 grid-cols-10 gap-4">
                    <div class="font-bold col-span-3">Arrivée</div>
                    <div class="col-span-7" :title="game?.target"
                         @mouseenter="hoverLink"
                         @mouseleave="unhoverLink">
                        {{ game?.target?.replaceAll('_', ' ') }}
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
                <div class="grid text-[#101010] pt-3 grid-cols-10 font-bold gap-4">
                    <div class="col-span-3">Joueur</div>
                    <div class="col-span-5">Page actuelle</div>
                    <div class="col-span-2 text-center"># Clics</div>

                </div>
            </h1>
            <ol>
                <!--                    <li v-for="(player, index) in [{username: 'Pelagoss'},{username: 'Pelagoss'}]" v-if="game.users != null">-->
                <li v-for="(player, index) in game.users">
                    <div class="grid text-[#101010] px-4 py-3 grid-cols-10 gap-4">
                        <div class="col-span-3">{{ player.username }}</div>
                        <div class="col-span-5 whitespace-nowrap text-ellipsis overflow-hidden">{{ game.clics[player.username].page }}</div>
                        <div class="col-span-2 text-center">{{ game.clics[player.username].clics }}</div>
                    </div>
                </li>
            </ol>
        </div>

        <div class="col-start-3 col-span-9" v-if="game?.is_started === true">
            <div v-if="!loading" ref="wiki"
                 class="mw-content-ltr sitedir-ltr ltr mw-body-content parsoid-body mediawiki mw-parser-output grid-col h-full"
                 :class="{'overflow-hidden h-[100vh]': game?.is_started === false}"
                 v-html="contenu">
            </div>

            <div v-else class="flex flex-col items-center justify-center h-full gap-6">
                <div class="scale-[2]">
                    <Loader></Loader>
                </div>
                Chargement...
            </div>
        </div>

        <div v-if="game?.winner !== null" class="modal-mask">
            <div class="flex flex-col gap-8 justify-center items-center modal-container">
                <Generique v-if="game != null" :start="game?.winner !== null" :game="game" @close="closeGame"/>
            </div>
        </div>

        <transition>
            <div ref="tooltip" class="mwe-popups mwe-popups-type-page mwe-popups-fade-in-up mwe-popups-no-image-pointer mwe-popups-is-not-tall absolute p-3"
                 style="display: none;height:fit-content;z-index:4000"
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
import Generique from "../components/Generique.vue";
import Loader from "../components/ui/Loader.vue";

export default {
    name: "Game",
    components: {Loader, Generique, IconeDynamiqueComposant, Button},
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
            game: {}
        }
    },
    computed: {
        ...mapState(userStore, {isAuthenticated: "isAuthenticated", username: "username"}),
    },
    mounted() {
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
            return;
        }

        if (this.isAuthenticated === true) {
            this.id = userStore().id;
            this.initSocket();
        }

        this.fetchPage(this.game.clics[userStore().username].page);


        var pages = document.getElementsByClassName('page');
        for(var i = 0; i < pages.length; i++)
        {
            var page = pages[i];
            if (i % 2 === 0)
            {
                page.style.zIndex = (pages.length - i);
            }
        }

        document.addEventListener('DOMContentLoaded', function(){
            for(var i = 0; i < pages.length; i++)
            {
                //Or var page = pages[i];
                pages[i].pageNum = i + 1;
            }
        })
    },
    created() {
        this.fetchGames();
    },
    methods: {
        closeGame() {
            this.destroy();

            this.$nextTick(() => {
                this.$router.push({name: 'accueil'});
            });
        },
        fetchGames() {
            this.loadPage = true;
            this.$axios.get('/games').then(({data}) => {
                this.games = data.reverse();
                userStore().games = this.games.filter(g => g.users.map(u => u.username).includes(userStore().username));
            }).finally(() => {
                this.loadPage = false;
            });
        },
        initSocket() {
            if (this.initStarted) {
                return;
            }

            this.initStarted = true;

            socket.connect();
            socket.on("connect", () => {
                socket.emit('join', this.game);
                this.socketJoined = true;
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
                this.$refs.premiere.classList.add('flipped');
                this.$refs.stats.classList.add('flipped');
                this.game = data;
            });

            socket.on('connect_error', (e) => {
                this.error = true;
            });

            this.initStarted = false;
        },
        destroy() {
            socket.disconnect();

            socket.off("connect");
            socket.off("PAGE_CHANGED");
            socket.off("GAME_FINISHED");
            socket.off("START_GAME");
        },
        launch() {

            this.$refs.door_un.classList.add('opened');
            this.$refs.door_deux.classList.add('opened');
            this.$refs.frame.classList.add('opened');

            setTimeout(() => {
                this.$refs.door_un.classList.remove('opened');
                this.$refs.door_deux.classList.remove('opened');
                this.$refs.frame.classList.remove('opened');
            }, 5000)
            // this.$axios.post('/game/launch').finally(() => {
            //     this.loading = false;
            // });
        },
        clickLink(event) {
            event.preventDefault();

            this.$refs.partie.classList.add('flipped');
            this.$refs.loadPage_un.classList.add('flipped');

            this.fetchPage(event.target['data-title']).finally(() => {
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.$refs.stats.classList.add('hidden');
                        this.$refs.stats.classList.remove('flipped');

                        this.$refs.partie.classList.add('hidden');
                        this.$refs.partie.classList.remove('flipped');

                        this.$nextTick(() => {
                            let fragmentPartie = document.createDocumentFragment();
                            fragmentPartie.appendChild(this.$refs.partie);

                            let fragmentStats = document.createDocumentFragment();
                            fragmentStats.appendChild(this.$refs.stats);

                            this.$refs.pages.append(fragmentStats);
                            this.$refs.pages.append(fragmentPartie);

                            this.$nextTick(() => {
                                this.$refs.stats.classList.remove('hidden');
                                setTimeout(() => {
                                    this.$refs.stats.classList.add('flipped');
                                    this.$refs.partie.classList.remove('hidden');

                                    this.$refs.loadPage_deux.classList.add('flipped');

                                    this.$nextTick(() => {
                                        this.$nextTick(() => {
                                            setTimeout(() => {
                                                let fragmentLoadUn = document.createDocumentFragment();
                                                let a = fragmentLoadUn.appendChild(this.$refs.loadPage_un);
                                                a.classList.add('hidden');
                                                a.classList.remove('flipped')
                                                a.classList.remove('hidden')

                                                let fragmentLoadDeux = document.createDocumentFragment();
                                                a = fragmentLoadDeux.appendChild(this.$refs.loadPage_deux);
                                                a.classList.add('hidden');
                                                a.classList.remove('flipped')
                                                a.classList.remove('hidden')

                                                this.$refs.pages.append(fragmentLoadUn);
                                                this.$refs.pages.append(fragmentLoadDeux);
                                            }, 1000)
                                        });
                                    });
                                }, 500)
                            });
                        });
                    }, 500)
                });
            });
        },
        hoverLink(event) {
            event.preventDefault();

            this.timeoutHover = setTimeout(() => {
                this.fetchLink(event);
            }, 250);
        },
        unhoverLink(event) {
            event.preventDefault();

            clearTimeout(this.timeoutHover);

            this.toggleTooltip(false, event)
        },
        fetchPage(title) {
            this.loading = true;
            return this.$axios.get('/game/page/' + title).then(({data}) => {
                this.contenu = data.replace(/<\/body>/, '').replace(/<body["'=\w0-9a-zA-Z-,_ ]*>/, '');
            }).finally(() => {
                this.loading = false;
            });
        },
        fetchLink(event) {
            if (event.target.title != null) {
                event.target["data-title"] = event.target.title;
                event.target.title = '';
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
                    this.$refs.tooltip.classList.add("flipped-x-y");
                    this.$refs.tooltip.classList.remove("flipped-x");
                    this.$refs.tooltip.classList.remove("flipped-y");

                    top = `auto`;
                    bottom = `${window.innerHeight - event.target.getBoundingClientRect().y + (event.target.offsetHeight / 2)}px`;
                    right = `${window.innerWidth - (event.target.getBoundingClientRect().x + 20)}px`;
                    left = `auto`;

                } else if (depasseY) {
                    this.$refs.tooltip.classList.add("flipped-y");
                    this.$refs.tooltip.classList.remove("flipped-x-y");
                    this.$refs.tooltip.classList.remove("flipped-x");

                    top = `auto`;
                    bottom = `${window.innerHeight - event.target.getBoundingClientRect().y + (event.target.offsetHeight / 2)}px`;
                    right = `auto`;
                    left = `${event.target.getBoundingClientRect().x}px`;
                } else if (depasseX) {
                    this.$refs.tooltip.classList.add("flipped-x");
                    this.$refs.tooltip.classList.remove("flipped-x-y");
                    this.$refs.tooltip.classList.remove("flipped-y");

                    top = `${event.target.getBoundingClientRect().y + event.target.offsetHeight + (event.target.offsetHeight / 3)}px`;
                    bottom = `auto`;
                    right = `${window.innerWidth - (event.target.getBoundingClientRect().x + 20)}px`;
                    left = `auto`;
                } else {
                    this.$refs.tooltip.classList.remove("flipped-x-y");
                    this.$refs.tooltip.classList.remove("flipped-y");
                    this.$refs.tooltip.classList.remove("flipped-x");

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

                if (event.target["data-title"] != null) {
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


/*--------------------
Leaderboard
--------------------*/
.leaderboard {
    position: fixed;
    width: 25%;
    height: max-content;
    border-radius: 10px;
    background-color: #6b6b6bf3;
    backdrop-filter: blur(20px);
}

.leaderboard h1 {
    font-size: 18px;
    color: #101010;
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