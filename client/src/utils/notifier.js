import {createApp, markRaw} from "vue";
import ToastContainer from "@/components/ui/ToastContainer.vue";

export const notifier = markRaw({
    install(app) {
        let toast = createApp(ToastContainer);
        let wrapper = document.createElement('div');
        wrapper.className = 'absolute bottom-0 pb-8 right-8 flex flex-col gap-3 overflow-hidden'
        let notifier = toast.mount(wrapper);

        if (document.body) {
            document.body.appendChild(wrapper);
        }

        app.provide('notifier', notifier);
        app.$notifier = notifier;
        app.config.globalProperties.$notifier = notifier;
    }
});