import { io } from "socket.io-client";

const URL = import.meta.env.VITE_SOCKET_URL;
const socket = io(URL, { autoConnect: false, transports: ['polling', 'flashsocket'] });
// const socket = io('localhost:5000');

socket.onAny((event, ...args) => {
    console.log(event, args);
});

export default socket;