import { defineRule } from 'vee-validate';
import { required, email, min } from '@vee-validate/rules';
import { localize } from '@vee-validate/i18n';

defineRule('required', required);
defineRule('email', email);
defineRule('min', min);

configure({
    // Generates an English message locale generator
    generateMessage: localize('en', {
        messages: {
            required: 'Ce champ est requis',
            min: 'Le champ doit au moins contenir {params} caractères',
            email: 'L\'adresse email est invalide',
        },
    }),
});