<template>
    <div id="login" class="bgTable h-full flex items-center justify-center m-auto relative">
        <div class="h-full w-1/2 absolute" :class="step === 'register' ? 'right-0' : 'right-[50%]'">
            <div class="text-5xl text-squadaOne font-black px-12 pt-16"><span
                class="text-white">WIKI</span><span
                class="text-accent">WARS</span></div>
            <div class="text-white text-base px-12 pb-16">Devenez un WikiJedi/WikiSith !</div>

            <div class="floating-img">
                <img src="/images/death_wiki_star.png" alt="floating death star">
            </div>
        </div>
        <div class="form h-full w-1/2 flex flex-col center z-10 absolute" :class="step === 'register' ? 'left-0' : 'left-[50%]'">
            <Form class="w-full">
                <template #fields>
                    <div class="w-full flex flex-col gap-6 center">
                        <span class="text-3xl font-bold tracking-wide">{{ step === 'login' ? 'Connexion' : 'Inscription'}}</span>
                        <TextField
                            v-if="step === 'register'"
                            name="email"
                            label="Email"
                            v-model="credentials.email"
                            help-text="Entrez votre email"
                            type="email"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            name="username"
                            label="Pseudo"
                            v-model="credentials.username"
                            help-text="Entrez votre pseudo"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            name="mdp"
                            label="Mot de passe"
                            v-model="credentials.password"
                            help-text="Entrez votre mot de passe"
                            type="password"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            v-if="step === 'register'"
                            name="mdpConfirm"
                            label="Confirmation du mot de passe"
                            v-model="credentials.passwordConfirm"
                            help-text="Confirmez votre mot de passe"
                            type="password"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <div class="mb-2 w-1/2 flex flex-col gap-2 flex flex-col">
                            <Button @click="submitForm" class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                                {{ step === 'login' ? 'Se connecter' : 'Créer mon compte'}}
                            </Button>

                            <div class="cursor-pointer text-xs text-grey0 hover:text-accent pt-4 w-fit" @click="flipMenu">
                                {{ step === 'login' ? 'Pas de compte ? Créez vous en un !' : 'Déjà un compte ? Connectez-vous !'}}
                            </div>
                        </div>
                    </div>
                </template>
            </Form>
        </div>
    </div>
</template>

<script>
import Button from "../components/ui/Button.vue";
import {mapActions} from "pinia";
import {userStore} from "../store/index.js";
import TextField from "../components/ui/form/TextField.vue";
import Form from "../components/ui/form/Form.vue";

export default {
    name: "Login",
    components: {TextField, Form, Button},
    data() {
        return {
            credentials: {},
            error: null,
            step: 'login'
        }
    },
    methods: {
        ...mapActions(userStore, {login: "login", register: "register"}),
        submitForm() {
            if (this.step === 'login'){
                this.login(this.credentials);
            } else if (this.step === 'register') {
                this.register(this.credentials);
            }
        },
        flipMenu() {
            this.step = this.step === 'login' ? 'register' : 'login';
        }
    },
}
</script>

<style lang="scss" scoped>
@import '../assets/style/style';

.floating-img {
    position: absolute;
    top: 35%;
    left: 35%;
    height: 35%;
    width: 35%;
    box-shadow: 0 5px 15px 0px rgba(0, 0, 0, 0.6);
    transform: translatey(0px);
    animation: float 5s ease-in-out infinite;
}

@keyframes float {
    0% {
        transform: translatey(0px);
    }
    50% {
        transform: translatey(-20px);
    }
    100% {
        transform: translatey(0px);
    }
}

#login {
    & * {
        transition: cubic-bezier(0,.15,.56,.77) 300ms;
    }
}

.center {
    @apply justify-center items-center;
}

.form {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
}
</style>