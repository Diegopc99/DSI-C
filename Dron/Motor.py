import rticonnextdds_connector as rti
import time
import threading
import navio.pwm

NUM_BUCLE = 500
THROTTLE_ARMADO = 0
YAW_ARMADO = 90
ARMADO = True

def Motor():
	
	with rti.open_connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor",url="config.xml") as connector:

		input = connector.get_input("Suscriptor::LectorRadio")
		print("<MOTOR> Waiting for publications...")
		input.wait_for_publications()
		print("<MOTOR> Waiting for data...")
		print("<MOTOR> Esperando secuencia de armado...")

		i = 0
		sigue = True

		while sigue:

			# Recogemos los datos
			input.wait()
			input.take()

			for sample in input.samples.valid_data_iter:
				data = sample.get_dictionary()
				yaw = data["Yaw"]
				throttle = data["Altura"]
				#print("<MOTOR> Posicion recibida del Altura: ",throttle)
				#print("<MOTOR> Posicion recibida del Yaw: ",yaw)

				if (yaw == YAW_ARMADO) and (throttle == THROTTLE_ARMADO):
					i += 1

				else:
					i = 0

				if i == NUM_BUCLE: 
					print("<MOTOR> ** EXITO EN LA SECUENCIA DE ARMADO **")
					ARMADO = False
					sigue = False

	
	# Lectura y paso de PWM al motor
	connector_motor = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
	input_mixer_motor = connector_motor.get_input("Suscriptor::LectorMixerMotor")

	while ARMADO:
		pass

	# Inicializamos el canal PWM del motor
	print("<MOTOR> PWM configuration")
	pwm = navio.pwm.PWM(4)
	time.sleep(0.1)
	pwm.initialize()
	time.sleep(0.1)
	pwm.set_period(50)
	time.sleep(0.1)
	pwm.enable()
	time.sleep(0.1)

	print("<MOTOR> *** EN 2 SEGUNDOS SE PONDRA A FUNCIONAR EL MOTOR ***")
	time.sleep(2)

	# Secuencia de arranque
	pwm.set_duty_cycle(1.2)
	time.sleep(0.1)

	connector_servos = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor",url="config.xml")
	input_mixer_servos = connector_servos.get_input("Suscriptor::LectorMixer")

	pwm1 = navio.pwm.PWM(0)
	pwm1.initialize()
	pwm2 = navio.pwm.PWM(1)
	pwm2.initialize()
	pwm3 = navio.pwm.PWM(2)
	pwm3.initialize()
	pwm4 = navio.pwm.PWM(3)
	pwm4.initialize()

	time.sleep(0.1)
	pwm1.set_period(50)
	pwm2.set_period(50)
	pwm3.set_period(50)
	pwm4.set_period(50)
	time.sleep(0.1)
	pwm1.enable()
	pwm2.enable()
	pwm3.enable()
	pwm4.enable()
	time.sleep(0.1)

	servo1 = 1.6
	servo2 = 1.6
	servo3 = 1.6
	servo4 = 1.6

	offset = 0


	while True:

		input_mixer_servos.wait() # wait for data on this input
		input_mixer_servos.take()

		for sample in input_mixer_servos.samples.valid_data_iter:

			data = sample.get_dictionary()
			servo1 = data["Servo1"]
			servo2 = data["Servo2"]
			servo3 = data["Servo3"]
			servo4 = data["Servo4"]
			#print("<MOTOR> Valores de los servos sin offset: ",servo1+offset," ",servo2+offset," ",servo3+offset," ",servo4+offset)
			#print("<MOTOR> Valores de los servos con offset: ",servo1," ",servo2," ",servo3," ",servo4)

	        pwm1.set_duty_cycle(servo1)
	        pwm2.set_duty_cycle(servo2)
	        pwm3.set_duty_cycle(servo3)
	        pwm4.set_duty_cycle(servo4)
	        #time.sleep(0.05)


		input_mixer_motor.wait()
		input_mixer_motor.take()

		for sample in input_mixer_motor.samples.valid_data_iter:
			data = sample.get_dictionary()
			velocidadMotor = data["VelocidadMotor"]
			#print("<MOTOR> Velocidad del motor recibida: ",velocidadMotor)

		# Pasamos al motor el valor del pulso PWM
		pwm.set_duty_cycle(velocidadMotor)
		#time.sleep(0.05)


if(__name__) == "__main__":
        Motor()



