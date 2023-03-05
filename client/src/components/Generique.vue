<template>
    <div class="back">
        <div :class="{'a-long-time-ago': start}">
            A long time ago, in a galaxy far,<br> far away..
        </div>

        <div :class="{'crawl': start}">
            <p>
                It is a period of civil war.
                Rebel spaceships, striking
                from a hidden base, have won
                their first victory against
                the evil Galactic Empire.
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: "Generique",
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
    width: 100%;
    height: 100%;
    background: black;
    margin: 0;
    overflow: hidden; /* Evite la scrollbar */

    /* Center items */
    display: flex;
    align-items: center;
    justify-content: center;
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
    left: 50%;
    width: 800px;
    margin: 0 0 0 -400px;
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
    animation-duration: 20s;
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
</style>