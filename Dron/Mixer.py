import rticonnextdds_connector as rti
import threading
import time

class Mixer:
	pitch_PID = 0
	roll_PID = 0
	yaw_PID = 0
	altitud_radio = 0
	last_yaw_PID = 0
	yaw_radio = 0

	def __init__(self):

		self.connector_suscriptor_PIDPitch = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_PIDRoll = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_PIDYaw = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_Mando = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_publicador = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml")
		self.connector_publicador_motor = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador",url="config.xml")
		self.output_mixer_motor = self.connector_publicador_motor.get_output("Publicador::EscritorMixerMotor")
		self.input_PID_pitch = self.connector_suscriptor_PIDPitch.get_input("Suscriptor::LectorPID_pitch")
		self.input_PID_roll = self.connector_suscriptor_PIDRoll.get_input("Suscriptor::LectorPID_roll")
		self.input_PID_yaw = self.connector_suscriptor_PIDYaw.get_input("Suscriptor::LectorPID_yaw")
		self.output_mixer = self.connector_publicador.get_output("Publicador::EscritorMixer")
		self.input_radio = self.connector_suscriptor_Mando.get_input("Suscriptor::LectorRadio")
		self.last_yaw_PID = 0.00
		self.last_ciclo = time.time() * 1000

	def getPID_pitch(self):
		
		while(True):
			# PID PITCH
			self.input_PID_pitch.wait()
			self.input_PID_pitch.take()

			for sample in self.input_PID_pitch.samples.valid_data_iter:
				data = sample.get_dictionary()
				self.pitch_PID = data["Pitch"]
				# print("<MIXER> Pitch recibido: ", self.pitch_PID)
			
			#ciclo_actual = time.time() * 1000

                        #print("Tiempo de ejecucion: ",(ciclo_actual - self.last_ciclo))
                        #self.last_ciclo = ciclo_actual


	def getPID_roll(self):
	
		while(True):
			# PID ROLL
			self.input_PID_roll.wait()
			self.input_PID_roll.take()

			for sample in self.input_PID_roll.samples.valid_data_iter:
				data = sample.get_dictionary()
				self.roll_PID = data["Roll"]
				# print("<MIXER> Roll recibido: ", self.roll_PID)
		
	def getPID_yaw(self):

		while(True):
			# PID YAW
			self.input_PID_yaw.wait()
			self.input_PID_yaw.take()

			for sample in self.input_PID_yaw.samples.valid_data_iter:
				data = sample.get_dictionary()
				self.yaw_PID = data["Yaw"]
				#print("<MIXER> Yaw recibido: ", self.yaw_PID)
	
	def getMando(self):

		while(True):
			# ALTURA / POTENCIA
			self.input_radio.wait()
			self.input_radio.take()

			for sample in self.input_radio.samples.valid_data_iter:
				data = sample.get_dictionary()
				self.altitud_radio = data["Altura"]
				self.yaw_radio = data["Yaw"]
				#print("<MIXER> Altura recibida: ", self.altitud_radio)


	def setServo(self):

		th = threading.Thread(target=self.getPID_pitch)
		th.daemon = True # Este hilo muere cuando el main finalize
		th.start()

		th1 = threading.Thread(target=self.getPID_roll)
		th1.daemon = True
		th1.start()

		th2 = threading.Thread(target=self.getPID_yaw)
		th2.daemon = True
		th2.start()
	
		th3 = threading.Thread(target=self.getMando)
		th3.daemon = True
		th3.start()
		
		while(True):

			self.pitch_PID = self.pitch_PID * 1
			self.roll_PID = self.roll_PID * 1
			self.yaw_PID = self.yaw_PID * 0.5 ## 0.5 mejor
			
			#if self.pitch_PID > 5:
			#	print("Pico en el pitch ",self.pitch_PID)
			#if self.roll_PID > 5:
			#	print("Pico en el roll ",self.roll_PID)
			#if self.yaw_PID > 5:
			#	print("Pico en el yaw: ",self.yaw_PID)

			#ciclo_actual = time.time() * 1000
		
			#print("Tiempo de ejecucion: ",(ciclo_actual - self.last_ciclo))
			#self.last_ciclo = ciclo_actual

			if (self.yaw_radio <= 2) and (self.yaw_radio >= -2): # El dron controla solo el giro porque el mando no envia nada

				self.yaw_PID =  0 - abs(self.yaw_PID)

				# BACK LEFT
				servo_value = self.pitch_PID + self.yaw_PID
				#if servo_value >= 45:
				#	servo_value = 45
	                        servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
	                        self.output_mixer.instance.set_number("Servo1", servo_value)

				# BACK RIGHT
                        	servo_value = self.roll_PID + self.yaw_PID
				#if servo_value >= 45:
                                #	servo_value = 45
				servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
                        	self.output_mixer.instance.set_number("Servo2", servo_value)

                        	# FRONT RIGHT
                                servo_value = -self.pitch_PID + self.yaw_PID
				#if servo_value >= 45:
                                #	servo_value = 45
                                servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
                                self.output_mixer.instance.set_number("Servo3", servo_value)

                        	# FRONT LEFT
                                servo_value = -self.roll_PID + self.yaw_PID
				#if servo_value >= 45:
                                #	servo_value = 45
                                servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
                                self.output_mixer.instance.set_number("Servo4", servo_value)


			if (self.yaw_radio >= 2) or (self.yaw_radio <= -2): # El giro del dron se controla con el mando


				# BACK LEFT
                		servo_value = self.pitch_PID + (self.yaw_PID)
				if servo_value >= 45:
                       	        	servo_value = 45
				servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
				self.output_mixer.instance.set_number("Servo1", servo_value)

				# BACK RIGHT
				servo_value = self.roll_PID + (self.yaw_PID)
				if servo_value >= 45:
                                	servo_value = 45
				servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
				self.output_mixer.instance.set_number("Servo2", servo_value)

				# FRONT RIGHT
				servo_value = -self.pitch_PID + (self.yaw_PID)
				if servo_value >= 45:
                                	servo_value = 45
				servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
				self.output_mixer.instance.set_number("Servo3", servo_value)

				# FRONT LEFT
				servo_value = -self.roll_PID + (self.yaw_PID)
				if servo_value >= 45:
                                	servo_value = 45
				servo_value = (((servo_value - (-90)) * (2.5 - 0.6)) / (90 - (-90))) + 0.6
				self.output_mixer.instance.set_number("Servo4", servo_value)


			# MOTOR
			motor_valor = (((self.altitud_radio - (0)) * (1.7 - 1.2))/ (100 - (0))) + 1.2
			self.output_mixer_motor.instance.set_number("VelocidadMotor", motor_valor)

			# SEND DATA
			self.output_mixer.write()
			self.output_mixer_motor.write()

			time.sleep(0.004)
	#def update_servos(self):
		
		#while True:
			#self.getValoresServos()
			#self.setServo()


if(__name__) == "__main__":
	mixerClass = Mixer()
	mixerClass.setServo()

