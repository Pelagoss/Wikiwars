<template>
    <div id="login" class="bgTable h-full flex items-center justify-center m-auto relative">
        <Modal persistent :closable="false" v-model="showModalConfirmation">
            <FormWrapper ref="form" class="w-full" @submit="$router.push({name: 'accueil'})">
                <template #fields>
                    <div class="flex flex-col items-center h-fit shadow-custom-elevate p-14">
                        <template v-if="loading === false && error === false">
                            <div class="text-5xl font-squadaOne text-center">
                                Inscription validée !
                            </div>

                            <div class="w-10 my-6 items-center">
                                <IconeDynamiqueComposant class="!w-10 !h-10" icon="CheckBadge"/>
                            </div>

                            <Button class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                                Connectez-vous !
                            </Button>
                        </template>

                        <template v-else-if="error === true">
                            <div class="text-4xl font-squadaOne text-center">
                                Une erreur est survenue !
                            </div>

                            <div class="mt-6 items-center">
                                Ce lien d'inscription est invalide ou expiré.
                            </div>

                            <div class="mt-2 mb-6 items-center">
                                Pour en recevoir un nouveau, essayez de vous connecter.
                            </div>

                            <Button class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                                Revenir à l'accueil
                            </Button>
                        </template>

                        <div v-else class="w-64 h-64 flex flex-col items-center">
                            <Loader></Loader>
                            <div class="font-squadaOne text-2xl">
                                Chargement ...
                            </div>
                        </div>
                    </div>
                </template>
            </FormWrapper>
        </Modal>
    </div>
</template>

<script setup>
import Button from "../components/ui/Button.vue"
import Modal from "../components/ui/Modal.vue"
import FormWrapper from "../components/ui/form/FormWrapper.vue"
import IconeDynamiqueComposant from "../components/IconeDynamiqueComposant.vue"
import {ref, inject} from "vue";
import {useRoute} from "vue-router";
import Loader from "../components/ui/Loader.vue";

const showModalConfirmation = ref(true);
const loading = ref(true);
const error = ref(false);
const $axios = inject('axios');

$axios.post('/register/confirm/' + useRoute().params.token).finally(() => {
    loading.value = false;
    error.value = false;
}).catch((r) => error.value = true);

</script>

<style lang="scss" scoped>
.center {
    @apply justify-center items-center;
}
</style>