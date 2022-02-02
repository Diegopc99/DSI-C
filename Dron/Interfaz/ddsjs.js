var rti   = require('rticonnextdds-connector');

const run = async () => {

	var connector = new rti.Connector("MyParticipantLibrary::ParticipanteSuscriptor",__dirname + "/config.xml");
	var input = connector.getInput("Suscriptor::LectorAttitude");

	console.log("Waiting for samples...");

	for (let i = 0; i < 500; i++){

		await input.wait()
		input.take()
    		for (const sample of input.samples.validDataIter) {
			const data = sample.getJson()
			const altura = sample.getNumber('Altura')
			const pitch = sample.getNumber('Pitch')
			const roll = sample.getNumber('Roll')
			const yaw = sample.getNumber('Yaw')

			console.log('Altura: '+altura+' | Pitch:' +pitch+' | Roll:' +roll+' | Yaw:' + yaw)
    		}
	}
	connector.close()
}

run()
