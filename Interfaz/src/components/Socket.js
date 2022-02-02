import io from "socket.io-client";
import React, {useState, useEffect} from "react";

const Socket = () =>{
    
    const URL = 'http://88.18.246.114:13000';
    const [response,setResponse] = useState("");

    const socket = io(URL);
    socket.on('connect', () => {
        console.log("I'm connected with the back-end");
        socket.on('disconnect', () => {
            console.log('user disconnected');
        });
    });

    useEffect(() =>{
    // Recibimos los valores por el canal prueba
        socket.on('Datos', (msg) => {
            console.log(msg);
            setResponse(msg);
        }); 
    },[]);

    return(
        <p> {response}</p>
    )
}

export default Socket;
