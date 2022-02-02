const WebSocket = require("ws");

const wss = new WebSocket.Server({port: 12000});

wss.on("connection", function(socket) {
    socket.on("message", function incoming(data) {
        
        const bytesString = data.toString('utf-8');
        console.log(bytesString);
        socket.send(bytesString);

    });
});

