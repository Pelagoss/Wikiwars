<template>
    <div class="grid grid-cols-12 h-[100vh]">
        <link rel="stylesheet" href="/wiki.css"/>

        <div class="book">
            <div id="pages" class="pages" ref="pages">
                <div class="page premiere" :class="{'flipped': game?.is_started || game?.winner !== null}" ref="premiere">
                    <div class="flex flex-col items-center justify-center h-full gap-6 relative text-white">
                        <div class="font-black absolute top-[10%] left-[15%] text-5xl"
                        style="font-family: Dancing Script;">
                            <div>
                                De {{ game?.start?.replaceAll('_', ' ') }} à
                            </div>
                            <div>
                                {{ game?.target?.replaceAll('_', ' ') }}
                            </div>
                        </div>
                        <div class="scale-[2]">
                            <Loader></Loader>
                        </div>

                        En attente du lancement de la partie...

                        <div class="text-light text-center font-bold my-3 flex justify-center items-center">
                            {{ game?.users?.length }} joueur(s)
                            <icone-dynamique-composant icon="User" class="ml-3 w-5 h-5"></icone-dynamique-composant>
                        </div>

                        <Button v-if="game?.host === id && game?.is_started === false && loadPage === false && socketJoined === true"
                                class="btnv-success"
                                @click="launch"
                        >
                            Start !
                        </Button>
                    </div>
                </div>
                <div class="page" :class="{'flipped': game?.is_started || game?.winner !== null}" ref="stats">
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
                </div>
                <div class="page" ref="partie" :class="{'flipped': game?.winner !== null}">
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

                <div class="page loader" :class="{'flipped': game?.winner !== null}" ref="loadPage_un">
                    <Loader></Loader>
                    Chargement...
                </div>
                <div class="page loader" :class="{'flipped': game?.winner !== null}" ref="loadPage_deux">
                    <Loader></Loader>
                    Chargement...
                </div>
            </div>
        </div>

        <div v-if="game?.winner !== null" class="modal-mask">
            <div class="flex flex-col gap-8 justify-center items-center modal-container">
                <Generique v-if="game != null" :start="game?.winner !== null" :game="game"/>
            </div>
        </div>

        <transition>
            <div ref="tooltip" class="mwe-popups mwe-popups-type-page mwe-popups-fade-in-up mwe-popups-no-image-pointer mwe-popups-is-not-tall absolute p-3"
                 style="display: block;height:fit-content;z-index:4000"
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
            socket: null,
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
        console.log("here");
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
            console.log("debut init")
            if (this.initStarted) {
                console.log("init abort")
                return;
            }

            this.initStarted = true;

            socket.connect();
            socket.on("connect", () => {
                console.log("SOCKET_CONNECTED");
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
        launch() {
            this.$axios.post('/game/launch').finally(() => {
                this.loading = false;
            });
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

            this.fetchLink(event);
        },
        unhoverLink(event) {
            event.preventDefault();

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
        console.log("DESTROY SOCKET");
        socket.disconnect();

        socket.off("connect");
        socket.off("PAGE_CHANGED");
        socket.off("GAME_FINISHED");
        socket.off("START_GAME");
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
    position: absolute;
    width: 100%;
    height: max-content;
    border-radius: 10px;
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


.book {
    transition: opacity 0.4s 0.2s;
    align-self: center;
}
.page {
    width: 30vw;
    height: 44vw;
    background-color: #111111;
    float: left;
    margin-bottom: 0.5em;
    background: left top no-repeat;
    background-size: cover;
}
.page:nth-child(even) {
    clear: both;
}
.book {
    perspective: 250vw;
    width: 100vw;
    overflow: hidden;
}
.book .pages {
    width: 98vw;
    height: 92vh;
    position: relative;
    transform-style: preserve-3d;
    backface-visibility: hidden;
    border-radius: 4px;
    /*box-shadow: 0 0 0 1px #e3dfd8;*/
}
.book .page {
    float: none;
    clear: none;
    margin: 0;
    position: absolute;
    top: 0;
    width: 50vw;
    height: 92vh;
    transform-origin: 0 0;
    transition: transform 1.4s;
    backface-visibility: hidden;
    transform-style: preserve-3d;
    user-select: none;
    background-color: #f0f0f0;
}
.book .page:nth-child(odd) {
    transform: rotateY(0deg);
    right: 0;
    border-radius: 20px 20px 32px 32px;
    background-image: linear-gradient(to right, rgba(0,0,0,.15) 0%, rgba(0,0,0,0) 10%);
    width: 74vw;
}
.book .page:nth-child(odd):before {
    background: rgba(0, 0, 0, 0);
}
.book .page:nth-child(even) {
    transform: rotateY(180deg);
    transform-origin: 100% 0;
    left: 0;
    border-radius: 20px 16px 12px 32px;
    border-color: black;
    background-image: linear-gradient(to left, rgba(0,0,0,.12) 0%, rgba(0,0,0,0) 10%);
    width: 24vw;
}
.book .page:nth-child(even):before {
    background: rgba(0, 0, 0, 0.2);
}
.book .page.grabbing {
    transition: none;
}
.book .page.flipped:nth-child(odd) {
    transform: rotateY(-180deg);
}
.book .page.flipped:nth-child(even) {
    transform: rotateY(0deg);
}
.page:nth-child(odd){
    background-position: right top;
}

.page.loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    color: #101010;

    &::v-deep(.lds-default div) {
        background: #101010 !important;
    }

    &::v-deep(.lds-default) {
        @apply scale-[2];
    }
}

.book #pages .page.premiere {
    background: #F33139;
    border-radius: 20px 16px 12px 32px;
    background-image: linear-gradient(to right,#D11F2F 130px, #ba0716 50px, transparent 50px);
}

//.page.premiere:before {
//    content: "";
//    background: #D11F2F!important;
//    height: 2rem;
//    width: 70%;
//    z-index: 6;
//    left: 20%;
//    box-shadow: 0px 73px #D11F2F;
//    position: absolute;
//    border-radius: 20px;
//    top: 10%;
//}

.page.premiere:after {
    content: "";
    position: absolute;
    background: white;
    border-radius: 32px 4px 4px 32px;
    box-shadow: inset 4px 6px 0px 0px #E4E0CE;
    background-image: linear-gradient(to bottom, transparent 6px, #E4E0CE 8px, transparent 8px, transparent 12px, #E4E0CE 12px, transparent 14px, transparent 18px,#E4E0CE 18px, transparent 20px, transparent 24px, #E4E0CE 24px, transparent 26px, transparent 30px, #E4E0CE 30px, transparent 32px, transparent 36px, #E4E0CE 36px, transparent 38px, transparent 42px, #E4E0CE 42px, transparent 44px, transparent 48px, #E4E0CE 48px, transparent 50px);
    height: 6vh;
    bottom: 9px;
    width: 99.5%;
    z-index: 5;
    right: 0;
}

.page.fin.flipped {
    width: 100vw!important;
}

</style>