import socketio from "socket.io-client";
import * as React from "react";

export const socket = socketio.connect('88.18.246.114:13000');
export const SocketContext = React.createContext();
