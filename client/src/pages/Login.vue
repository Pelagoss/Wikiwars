<template>
    <div id="login" class="bgTable h-full flex items-center justify-center m-auto">
        <div class="h-full w-1/2">
                <div class="text-3xl font-black px-12 pt-16"><span
                    style="color: white; font-family: 'Squada One', cursive;">WIKI</span><span
                    style="color: #008b2a; font-family: 'Squada One', cursive;">WARS</span></div>
                <div class="text-white text-base px-12 pb-16">Bienvenue sur WikiWars, connectez-vous !</div>
        </div>
        <div class="form h-full w-1/2 flex flex-col center">
            <Form class="w-full">
                <template #fields>
                    <div class="w-full flex flex-col gap-4 center">
                        <TextField
                            v-if="step === 'register'"
                            name="email"
                            label="Email"
                            v-model="credentials.email"
                            help-text="Entrez votre email"
                            type="email"
                            class="w-1/2"
                        ></TextField>

                        <TextField
                            name="username"
                            label="Pseudo"
                            v-model="credentials.username"
                            help-text="Entrez votre pseudo"
                            class="w-1/2"
                        ></TextField>

                        <TextField
                            name="mdp"
                            label="Mot de passe"
                            v-model="credentials.password"
                            help-text="Entrez votre mot de passe"
                            type="password"
                            class="w-1/2"
                        ></TextField>

                        <TextField
                            v-if="step === 'register'"
                            name="mdpConfirm"
                            label="Confirmation du mot de passe"
                            v-model="credentials.passwordConfirm"
                            help-text="Confirmez votre mot de passe"
                            type="password"
                            class="w-1/2"
                        ></TextField>

                        <div class="mb-2 w-1/2 flex flex-col">
                            <Button @click="submitForm" class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                                {{ step === 'login' ? 'Se connecter' : 'Créer mon compte'}}
                            </Button>

                            <div class="cursor-pointer text-xs text-[#6c757d] pt-4" @click="flipMenu">
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

.center {
    @apply justify-center items-center;
}

.form {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
}
</style>