const express = require('express');
const cors = require('cors');
const rti = require('rticonnextdds-connector');

const app = express();
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server,{
	cors: {
		origin: '*',
	}
});

const connector = new rti.Connector("MyParticipantLibrary::ParticipanteSuscriptor","../config.xml");
const input = connector.getInput("Suscriptor::LectorAttitude");
const connector_int = new rti.Connector("MyParticipantLibrary::ParticipantePublicador","../config.xml");
const output = connector_int.getOutput("Publicador::EscritorInterfaz");

app.use(cors({
	origin: '*'
}));

var kp_pitch, kp_roll, kp_yaw = 0;
var ki_pitch, ki_roll, ki_yaw = 0;
var kd_pitch, kd_roll, kd_yaw = 0;
var wg_pitch, wg_roll, wg_yaw = 0;

io.on('connection', (socket) => {
	console.log('a user connected');
	socket.emit("Datos","Socket conectado");
	
	socket.on("kp_pitch", (kp_pitch) => {
		console.log("Mensaje de kp del pitch: ", kp_pitch);
		output.instance.setNumber('kp_pitch', parseFloat(kp_pitch));
		//output.write();
	});

	socket.on("ki_pitch", (ki_pitch) => {
                console.log("Mensaje de ki del pitch: ", ki_pitch);
		output.instance.setNumber('ki_pitch',parseFloat(ki_pitch));
		//output.write();
        });

	socket.on("kd_pitch", (kd_pitch) => {
                console.log("Mensaje de kd del pitch: ", kd_pitch);
		output.instance.setNumber('kd_pitch',parseFloat(kd_pitch));
		//output.write();
        });
        socket.on("kp_roll", (kp_roll) => {
                console.log("Mensaje de kp del roll: ", kp_roll);
                output.instance.setNumber('kp_roll', parseFloat(kp_roll));
                //output.write();
        });

        socket.on("ki_roll", (ki_roll) => {
                console.log("Mensaje de ki del roll: ", ki_roll);
                output.instance.setNumber('ki_roll',parseFloat(ki_roll));
                //output.write();
        });
        socket.on("kd_roll", (kd_roll) => {
                console.log("Mensaje de kd del roll: ", kd_roll);
                output.instance.setNumber('kd_roll',parseFloat(kd_roll));
                //output.write();
        });
        socket.on("kp_yaw", (kp_yaw) => {
                console.log("Mensaje de kp del yaw: ", kp_yaw);
                output.instance.setNumber('kp_yaw', parseFloat(kp_yaw));
                //output.write();
        });

        socket.on("ki_yaw", (ki_yaw) => {
                console.log("Mensaje de ki del yaw: ", ki_yaw);
                output.instance.setNumber('ki_yaw',parseFloat(ki_yaw));
                //output.write();
        });
        socket.on("kd_yaw", (kd_yaw) => {
                console.log("Mensaje de kd del yaw: ", kd_yaw);
                output.instance.setNumber('kd_yaw',parseFloat(kd_yaw));
                //output.write();
        });
	socket.on("wg_pitch", (wg_pitch) => {
		console.log("Mensaje de windup guard del pitch", wg_pitch);
		output.instance.setNumber("wg_pitch", parseFloat(wg_pitch));
		//output.write();
	});
	socket.on("wg_roll", (wg_roll) => {
		console.log("Mensaje de windup guard del roll", wg_roll);
		output.instance.setNumber("wg_roll", parseFloat(wg_roll));
		//output.write();
	});
	socket.on("wg_yaw", (wg_yaw) => {
		console.log("Mensaje de windup guard del yaw", wg_yaw);
		output.instance.setNumber("wg_yaw", parseFloat(wg_yaw));
		//output.write();
	});

	socket.on("update_pitch", (msg) => {
                console.log("Mensaje: ", msg);
                //output.instance.setNumber('kd',parseFloat(kd));
                output.write();
        });
	socket.on("update_roll", (msg) => {
		console.log("Mensaje: ", msg);
		output.write();

	});
	socket.on("update_yaw", (msg) => {
		console.log("Mensaje: ", msg);
		output.write();
	});

});

server.listen(13000, () => {
	console.log('listening on 13000');
});

connector.on('on_data_available', () => {
  // We have received data on one of the inputs within this connector
  // Iterate through each one, checking if it has any valid data

    input.take()
    for (const sample of input.samples.validDataIter) {
	const data = sample.getJson()
        const altura = sample.getNumber('Altura')
        const pitch = sample.getNumber('Pitch')
        const roll = sample.getNumber('Roll')
        const yaw = sample.getNumber('Yaw')

        datos = ""+altura+',' +pitch+',' +roll+',' + yaw;

     	io.sockets.emit("Datos", datos);
    }
})
