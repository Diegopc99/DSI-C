import time
import sys
import array
import navio.ms5611
import navio.util
import rticonnextdds_connector as rti

with rti.open_connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml") as connector:

	output = connector.get_output("Publicador::EscritorRadio")

	while True:

		channel_values = []

		for i in range (0,4):

			f = open("/sys/kernel/rcio/rcin/ch%d" % i,"r")
			channel_values.append(float(f.read()))
			# print(channel_values[i])

		# Formula para convertir el rango de 1104 a 1924 a un rango en grados de 90 a -90
		# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

		roll = (((channel_values[0] -1104) * (90 - (-90))) / (1924 - 1104)) + (-90)
		pitch = (channel_values[1] -1104) * (90 - (-90)) / (1924 - 1104) + (-90)
		throttle = (channel_values[2] -1104) * (100 - (0)) / (1924 - 1104) + (0)
		yaw = (channel_values[3] -1104) * (90 - (-90)) / (1924 - 1104) + (-90)

		#print("<RADIO> Data to be sent through DDS: Datos del modulo Radio")
		#print("<RADIO> Roll: ",roll)
		#print("<RADIO> Pitch: ",pitch)
		#print("<RADIO> Yaw: ",yaw)
		#print("<RADIO> Throttle: ",throttle)
		output.instance.set_number("Roll", roll)
		output.instance.set_number("Pitch",pitch)
		output.instance.set_number("Yaw",yaw)
		output.instance.set_number("Altura",throttle)
		output.write()
		time.sleep(0.004)

	print("Exiting...")

