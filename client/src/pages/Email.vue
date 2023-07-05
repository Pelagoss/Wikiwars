<template>
    <div id="login" class="bgTable h-full flex items-center justify-center m-auto relative">
        <Modal persistent :closable="false" v-model="showModalConfirmation">
            <div v-if="error === false" v-html="mailContent"></div>
            <FormWrapper v-else ref="form" class="w-full" @submit="$router.push({name: 'accueil'})">
                <template #fields>
                    <div class="flex flex-col items-center h-fit shadow-custom-elevate p-14">
                        <div class="text-4xl font-squadaOne text-center">
                            Une erreur est survenue !
                        </div>

                        <div class="my-6 items-center">
                            Cet email n'est pas accessible ou est supprimé.
                        </div>

                        <Button class="btnv-success !w-full justify-center" icon="ArrowRightCircle">
                            Revenir à l'accueil
                        </Button>
                    </div>
                </template>
            </FormWrapper>
        </Modal>
    </div>
</template>

<script setup>
import Modal from "../components/ui/Modal.vue"
import Button from "../components/ui/Button.vue"
import {ref, inject} from "vue";
import {useRoute} from "vue-router";
import FormWrapper from "../components/ui/form/FormWrapper.vue";

const showModalConfirmation = ref(true);
const loading = ref(true);
const error = ref(false);
const mailContent = ref('');
const $axios = inject('axios');

$axios.post('/email/download/' + useRoute().params.token)
    .then((r) => {
        mailContent.value = r.data;
    })
    .finally(() => {
    loading.value = false;
    error.value = false;
}).catch((r) => error.value = true);

</script>

<style lang="scss" scoped>
.center {
    @apply justify-center items-center;
}
</style>