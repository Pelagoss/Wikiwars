import { io } from "socket.io-client";

const URL = "localhost:5000";
const socket = io(URL, { autoConnect: false, transports: ['polling', 'flashsocket'] });
// const socket = io('localhost:5000');

socket.onAny((event, ...args) => {
    console.log(event, args);
});

export default socket;