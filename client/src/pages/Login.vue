<template>
    <div id="login" class="bgTable h-full flex items-center justify-center m-auto relative">
        <div class="h-full w-1/2 absolute" :class="step === 'register' ? 'right-0' : 'right-[50%]'">
            <div class="text-5xl font-squadaOne font-black px-12 pt-16"><span
                class="text-white">WIKI</span><span
                class="text-accent">WARS</span></div>
            <div class="text-white text-base px-12 pb-16">Devenez un WikiJedi/WikiSith !</div>

            <div class="floating-img">
                <img src="/images/death_wiki_star.png" alt="floating death star">
            </div>
        </div>
        <div class="form h-full w-1/2 flex flex-col center z-10 absolute" :class="step === 'register' ? 'left-0' : 'left-[50%]'">
            <FormWrapper :error="error" ref="form" class="w-full" @submit="submitForm">
                <template #fields>
                    <div class="w-full flex flex-col gap-6 center">
                        <span class="text-4xl font-squadaOne font-bold tracking-widest">{{ step === 'login' ? 'Connexion' : 'Inscription'}}</span>
                        <TextField
                            v-if="step === 'register'"
                            rules="required|email"
                            name="email"
                            label="Email"
                            v-model="credentials.email"
                            help-text="Entrez votre email"
                            type="email"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            rules="required"
                            name="username"
                            label="Pseudo"
                            v-model="credentials.username"
                            help-text="Entrez votre pseudo"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            rules="required|oneUpper|oneLower|oneDigit|min:7"
                            name="password"
                            label="Mot de passe"
                            v-model="credentials.password"
                            help-text="Entrez votre mot de passe"
                            type="password"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <TextField
                            v-if="step === 'register'"
                            rules="confirmed:@password"
                            name="passwordConfirm"
                            label="Confirmation du mot de passe"
                            v-model="credentials.passwordConfirm"
                            help-text="Confirmez votre mot de passe"
                            type="password"
                            class="w-1/2 flex flex-col gap-2"
                        ></TextField>

                        <div class="mb-2 w-1/2 flex flex-col gap-2 flex flex-col">
                            <Button :loading="loading" class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                                {{ step === 'login' ? 'Se connecter' : 'Créer mon compte'}}
                            </Button>

                            <div class="cursor-pointer text-xs text-grey0 hover:text-accent pt-4 w-fit" @click="flipMenu">
                                {{ step === 'login' ? 'Pas de compte ? Créez vous en un !' : 'Déjà un compte ? Connectez-vous !'}}
                            </div>
                        </div>
                    </div>
                </template>
            </FormWrapper>
        </div>

        <Modal v-model="showModalConfirmation">
            <div class="flex flex-col items-center h-fit shadow-custom-elevate p-14">
                <div class="text-5xl font-squadaOne text-center">
                    Merci !
                </div>

                <div class="w-8 mt-6 mb-3">
                    <IconeDynamiqueComposant class="w-5 h-5" icon="EnvelopeOpen"/>
                </div>

                <div class="text-white font-medium text-center">
                    Validez votre compte via l’email qui vous a été<br class="sm:hidden">
                    envoyé pour accéder à votre espace client.
                </div>
            </div>
        </Modal>
    </div>
</template>

<script>
import Button from "../components/ui/Button.vue";
import {mapActions} from "pinia";
import {userStore} from "../store/index.js";
import TextField from "../components/ui/form/TextField.vue";
import Form from "../components/ui/form/FormWrapper.vue";
import FormWrapper from "../components/ui/form/FormWrapper.vue";
import Modal from "../components/ui/Modal.vue";
import IconeDynamiqueComposant from "../components/IconeDynamiqueComposant.vue";

export default {
    name: "Login",
    components: {IconeDynamiqueComposant, Modal, FormWrapper, TextField, Form, Button},
    data() {
        return {
            credentials: {},
            error: null,
            step: 'login',
            loading: false,
            showModalConfirmation: false
        }
    },
    methods: {
        ...mapActions(userStore, {login: "login", register: "register"}),
        submitForm() {
            this.loading = true;
            if (this.step === 'login'){
                this.login(this.credentials).catch((e) => {
                        console.log(e);
                        if (e.response.status === 401) {
                            this.error = e.response.data.message.replaceAll('[username]', 'Le pseudo')
                                .replaceAll('[email]', 'L\'adresse email')
                        }
                    }
                );
            } else if (this.step === 'register') {
                this.error = null;
                this.register(this.credentials)
                    .then(({data}) => {
                        if (data === true) {
                            this.showModalConfirmation = true;
                            this.step = 'login';
                        }
                    })
                    .catch((e) => {
                            console.log(e);
                            if (e.response.status === 403) {
                                let error = {};

                                error[e.response.data.field] = e.response.data.message.replaceAll('[username]', 'Le pseudo')
                                    .replaceAll('[email]', 'L\'adresse email');
                                this.$refs.form.$refs.form.setErrors(error);
                                this.error = e.response.data.message.replaceAll('[username]', 'Le pseudo')
                                    .replaceAll('[email]', 'L\'adresse email')
                            } else {
                                this.error = e.response.data.message.replaceAll("["+e.response.data.field+"]", this.errorMessage[e.response.data.field]);
                            }
                        }
                    );
            }
            this.loading = false;
        },
        flipMenu() {
            this.error = '';
            this.step = this.step === 'login' ? 'register' : 'login';
        }
    },
    computed: {
        errorMessage() {
            return {
                'email': 'email',
                'username': 'pseudo',
                'password': 'mot de passe',
                'passwordConfirm': 'confirmation du mot de passe'
            }
        }
    }
}
</script>

<style lang="scss" scoped>
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