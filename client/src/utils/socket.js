import { io } from "socket.io-client";

const URL = "http://127.0.0.1:5000/";
// const socket = io(URL, { autoConnect: false, transports: ['websocket', 'polling', 'flashsocket'] });
const socket = io('localhost:5000');

socket.onAny((event, ...args) => {
    console.log(event, args);
});

export default socket;