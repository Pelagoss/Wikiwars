import {configure, defineRule} from 'vee-validate';
import { required, email, min, confirmed } from '@vee-validate/rules';
import { localize } from '@vee-validate/i18n';

configure({
    // Generates an English message locale generator
    generateMessage: localize({
        'en': {
            messages: {
                required: 'Ce champ est requis',
                min: 'Le champ doit contenir au moins {params} caractères',
                email: 'L\'adresse email est invalide',
                oneUpper: 'Le champ doit contenir au moins 1 majuscule',
                oneLower: 'Le champ doit contenir au moins 1 minuscule',
                oneDigit: 'Le champ doit contenir au moins 1 chiffre',
                confirmed: 'Le champ doit être identique au champ mot de passe',
            },
        }
    }),
});

defineRule('required', required);
defineRule('email', email);
defineRule('min', min);
defineRule('confirmed', confirmed);

defineRule('oneUpper', (v) => {
    let strongRegex = new RegExp("[A-Z]");
    return strongRegex.test(v);
})
defineRule('oneLower', (v) => {
    let strongRegex = new RegExp("[a-z]");
    return strongRegex.test(v);
})
defineRule('oneDigit', (v) => {
    let strongRegex = new RegExp("[0-9]");
    return strongRegex.test(v);
})