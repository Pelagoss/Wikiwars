<template>
    <div class="bgTable h-full flex items-center justify-center m-auto">
        <div class="h-1/3 w-1/3 flex">
            <div class="rounded w-1/2 my-4 bg-[#101010] flex flex-col justify-between">
                <div class="text-3xl font-black px-12 pt-16"><span
                    style="color: white; font-family: 'Squada One', cursive;">WIKI</span><span
                    style="color: #008b2a; font-family: 'Squada One', cursive;">WARS</span></div>
                <div class="text-white text-base px-12 pb-16">Bienvenue sur WikiWars, connectez-vous !</div>
            </div>
            <div class="rounded w-1/2 h-full bg-[#1b1e24] px-12 py-8">
                <div class="w-full flex flex-col items-center">
                    <div class="mb-4">
                        <label for="inputPseudo" class="text-base">Pseudo</label>

                        <div class="input-form">
                            <input v-model="credentials.inputPseudo" name="inputPseudo" type="text" required="required" id="inputPseudo">
                        </div>

                        <div id="inputPseudoHelp" class="text-xs text-[#6c757d]">Entrez votre pseudo</div>
                    </div>

                    <div class="mb-4">
                        <label for="inputPwd" class="form-label">Mot de passe</label>

                        <div class="input-form">
                            <input v-model="credentials.inputPwd" name="inputPwd" type="password" required="required" id="inputPwd">
                        </div>
                        <div id="inputPwdHelp" class="text-xs text-[#6c757d]">Entrez votre mot de passe</div>
                    </div>

                    <div class="mb-2">
                        <Button @click="login(credentials)" class="btnv-success" icon="Play">
                            Se connecter
                        </Button>
                    </div>

                    <div v-if="error !== null" class="self-start text-red-400 text-xs" style="display: block">
                        {{ error }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Button from "./ui/Button.vue";
import {mapActions} from "pinia";
import {userStore} from "../store/index.js";

export default {
    name: "Login",
    components: {Button},
    data() {
        return {
            credentials: {},
            error: null
        }
    },
    methods: {
        ...mapActions(userStore, {login: "login"})
    },
}
</script>

<style lang="scss" scoped>
label {
    color: #c2c2c5;
}

input {
    background: transparent;
    border: 0;
    color: #f2f2f2;
    font-size: 1rem;
    height: 1.5rem;
    line-height: 1.25rem;
    outline: none !important;
    width: 100%;
}

.input-form {
    &:after {
        content: "";
        display: block;
        width: 100%;
        height: 0.25rem;
        background: linear-gradient(to right, #12dd60, #008b2a);
    }
}

.bgTable {
    background: url("/table_bg.gif") no-repeat center;
    background-size: cover;
}

</style>