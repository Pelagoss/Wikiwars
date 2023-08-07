import { io } from "socket.io-client";
import {reactive} from "vue";
import {emitter} from "./index.js";
import {friendsStore} from "@/store/index.js";

export const state = reactive({
    connected: false,
});

const URL = import.meta.env.VITE_SOCKET_URL;
export const socket = io(URL, { autoConnect: false, withCredentials: true, transports: ['polling', 'flashsocket'] });

// const socket = io('localhost:5000');

socket.on("connect", () => {
    state.connected = true;
    emitter.$emit("SOCKET_CONNECTED", true);
});

socket.on("disconnect", () => {
    state.connected = false;
});

socket.on('NEW_FRIEND', () => {
    friendsStore().fetchFriends();
});

socket.onAny((event, ...args) => {
    console.log(event, args);
});