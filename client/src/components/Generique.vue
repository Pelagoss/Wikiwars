<template>
    <div class="back">
        <div :class="{'a-long-time-ago': start}">
            A long time ago, in a galaxy far,<br> far away..
        </div>

        <div :class="{'crawl': start}">
            <div>
                <p>Le valeureux joueur {{ game?.winner?.username }} à réussi à ne faire qu'un avec la force !</p>
                <p>Sa capacité à maitriser la force lui a permis de remplir sa mission...</p>
                <p>
                    {{ game?.winner?.username }} a traversé la galaxie à bord du Faucon Millenium pour rallier {{game?.target?.replaceAll('_', ' ')}} depuis
                    {{ game?.start?.replaceAll('_', ' ') }} !
                </p>
                <p v-if="game?.users?.filter(u => u.username !== game?.winner?.username)?.length !== 0">
                    Il aura au passage écrasé bon nombre de Sith (web) tels que : {{game?.users?.filter(u => u.username !== game?.winner?.username).map(u => u.username).join(', ')}}.
                </p>
            </div>
        </div>

        <div class="the-end text-white flex flex-col items-center gap-6">
            <div class="text-lg font-bold">
                GG {{ game?.winner?.username }} !
            </div>

            <Button
                class="btnv-4"
                @click="$emit('close')"
            >
                Quitter
            </Button>
        </div>
    </div>
</template>

<script>
import Button from "../components/ui/Button.vue";

export default {
    name: "Generique",
    components: {Button},
    props: {
        start: {
            type: Boolean,
            default: false
        },
        game: {
            type: Object
        }
    }
}
</script>

<style scoped>
.back {
    position: relative;
    width: 100%;
    height: 100%;
    background: black;
    margin: 0;
    overflow: hidden; /* Evite la scrollbar */

    /* Center items */
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.a-long-time-ago {
    /* cosmétique */
    font-size: 32px;
    color: #4bd5ee;
    /* Animation */
    /* Apparition et disparition progressive */
    opacity: 0;
    animation-delay: 1s;
    animation-duration: 1s;
    animation-name: a-long-time-ago;
    animation-timing-function: ease-out;
}

@keyframes a-long-time-ago {
    0% {
        opacity: 0;
    }

    20% {
        opacity: 1;
    }

    80% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.crawl {
    /* centrage de l'élément' */
    position: absolute;
    top: 45%;
    left: 25%;
    width: 50%;
    top: auto;
    bottom: 0;
    height: 50em;
    /* cosmétique */
    color: #ffff66;
    font-size: 64px;
    text-align: justify;
    /* Applique la transformation  */
    transform-origin: center bottom;
    transform: perspective(300px) rotateX(25deg);
}

.crawl > div {
    /* positionne la div en bas de l'écran (non visible) */
    /* l'animation la fait remonter progressivement */
    position: absolute;
    top: 100%;
    animation-delay: 2s; /* Démarre l'animation après la première */
    animation-duration: 15s;
    animation-name: crawl;
    animation-timing-function: linear;
}

@keyframes crawl {
    0% {
        top: 100%;
        opacity: 1;
    }

    80% {
        opacity: 1; /* disparition progressive à la fin */
    }

    100% {
        top: 0;
        opacity: 0;
    }
}

.the-end {
    opacity: 1;
    animation-delay: 0s;
    animation-duration: 17s;
    animation-name: the-end;
}

@keyframes the-end {
    0% {
        opacity: 0;
    }

    90% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>