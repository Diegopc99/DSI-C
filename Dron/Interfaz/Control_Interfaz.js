const express = require('express');
const cors = require('cors');
//const rti = require('rticonnextdds-connector');

const io = require("socket.io-client");
const ioClient = io.connect("http://88.18.242.134:13000"); //Posiblemente hay que cambiar el puerto

var msg = "hello";/*
ioClient.emit('Datos',msg);*/

var msg2 = "hey";
ioClient.on('connect', (msg) => { //Mensaje de que se ha conectado ?
		console.log(msg);
});

ioClient.on('Datos', (msg2) => { //Datos que recibe del servidor
		console.log(msg2);
});
