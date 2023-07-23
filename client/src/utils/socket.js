import { io } from "socket.io-client";
import {reactive} from "vue";
import {emitter} from "./index.js";

export const state = reactive({
    connected: false,
});

const URL = import.meta.env.VITE_SOCKET_URL;
export const socket = io(URL, { autoConnect: false, transports: ['polling', 'flashsocket'] });
// const socket = io('localhost:5000');

socket.on("connect", () => {
    state.connected = true;
    emitter.$emit("SOCKET_CONNECTED", true);
});

socket.onAny("disconnect", () => {
    state.connected = false;
});

socket.onAny((event, ...args) => {
    console.log(event, args);
});