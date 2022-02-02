import rticonnextdds_connector as rti
import threading
import time
from pykalman import KalmanFilter 

class PID_Roll:


	def __init__(self):

		self.initializate_default_values()

		# DDS
		self.connector_suscriptor_radio = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_attitude = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_interfaz = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_publicador = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml")	
		self.input_radio = self.connector_suscriptor_radio.get_input("Suscriptor::LectorRadio")
		self.input_attitude = self.connector_suscriptor_attitude.get_input("Suscriptor::LectorAttitude")
		self.output_pid = self.connector_publicador.get_output("Publicador::EscritorPID_roll")
		self.input_interfaz = self.connector_suscriptor_interfaz.get_input("Suscriptor::LectorInterfaz")


	def getRoll_mando(self):

		while(True):
			# Esperamos por el dato ROLL del MANDO
			self.input_radio.wait()
			self.input_radio.take()

			# Guardamos el valor de ROLL-radio
			for sample in self.input_radio.samples.valid_data_iter:
				data = sample.get_dictionary()
				roll_mando = data["Roll"]
				#print("<PID-ROLL> Posicion recibida: ", roll_mando)
			
			self.setPoint = roll_mando


	def getRoll_attitude(self):

		while(True):
			# Esperamos por el dato ROLL del modulo AHRS
			self.input_attitude.wait()
			self.input_attitude.take()

			# Guardamos el valor de ROLL-AHRS
			for sample in self.input_attitude.samples.valid_data_iter:
				data = sample.get_dictionary()
				roll_attitude = data["Roll"]
				#print("<PID-ROLL> Posicion recibida Attitude: ", roll_attitude)
			
			self.feedbackValue = roll_attitude
		#return (roll_mando, roll_attitude)


	def initializate_default_values(self):

		# reiniciamos variables
		self.Kp = 0.6
		self.Ki = 0.4
		self.Kd = 0.3
		self.Pterm = 0.00
		self.Iterm = 0.00
		self.Dterm = 0.00
		self.sample_time = 4
		self.current_time = None
		self.last_time = None
		self.last_output = 0.00
		self.last_error = 0.00
		self.windup_guard = 2
		self.array_filter = [0,0,0]
		self.kalman_window = [0,0,0]
		self.setPoint = 0.00
		self.feedbackValue = 0.00

	def update_const(self):

		while True:
			print("<PID-ROLL> Esperando publicaciones de K")
			#self.input_interfaz.wait_for_publications()
			self.input_interfaz.wait()
			self.input_interfaz.take()

			for sample in self.input_interfaz.samples.valid_data_iter:
				data = sample.get_dictionary()
				if data["kp_roll"] != 0:
					self.Kp = data["kp_roll"]
				if data["kd_roll"] != 0:
					self.Kd = data["kd_roll"]
				if data["ki_roll"] != 0:
					self.Ki = data["ki_roll"]
				if data["wg_roll"] != 0:
					self.windup_guard = data["wg_roll"]

			print("<PID-ROLL> Actualizados valores de K")
			print("<PID-ROLL> self.kp: ",self.Kp)
			print("<PID-ROLL> self.kd: ",self.Kd)
			print("<PID-ROLL> self.ki: ",self.Ki)
			print("<PID-ROLL> self.windup_guard: ", self.windup_guard)

	def update(self):

		th = threading.Thread(target=self.update_const)
		th.daemon = True # Este hilo muere cuando el main finalize
		th.start()

		th1 = threading.Thread(target=self.getRoll_attitude)
		th1.daemon = True
		th1.start()

		th2 = threading.Thread(target=self.getRoll_mando)
		th2.daemon = True
		th2.start()

		first_loop = True

		print("<PID-ROLL> Comenzamos el bucle de calculo del PID")

		while True:
			# Conseguimos los valores del roll de mando y del modulo AHRS y calculamos el error
			#(setPoint, feedbackValue) = self.getRoll()
			error = self.setPoint - self.feedbackValue

			self.current_time = time.time() * 1000
			self.last_time = self.current_time if self.last_time is None else self.last_time

			# diferencia entre ahora y la ultima vez que hicimos calculos
			delta_time = self.current_time - self.last_time

			# diferencia entre error de ahora con el anterior guardado
			delta_error = error - self.last_error

			# miramos si ha transcurrido el tiempo que hemos establecido como intervalo
			if(delta_time >= self.sample_time):

				# calculamos control proporcional
				self.PTerm = self.Kp * error

				# calculo control integral
				self.Iterm += error * delta_time
				#print("ITerm: ", self.Iterm)

				# miramos si Iterm no esta por encima o por debajo del intervalo que consideremos como coherente
				if(self.Iterm < -self.windup_guard):
					self.Iterm = -self.windup_guard

				elif (self.Iterm > self.windup_guard):
					self.Iterm = self.windup_guard

				self.DTerm = 0.0

				if delta_time > 0:
					self.DTerm = delta_error / delta_time

				# guardamos parametros para proximo calculo
				self.last_time = self.current_time
				self.last_error = error

				# hacemos calculo del PID
				self.output = self.PTerm + (self.Ki * self.Iterm) + (self.Kd * self.DTerm)
				#print("<PID-ROLL> Output before filter: ", self.output)

				if first_loop == True:

					self.array_filter.insert(0, self.output)
					self.array_filter.pop()

				if first_loop == False:

					if self.output > 90:
						self.output = self.last_output
					elif self.output < -90:
						self.output = self.last_output

				# Filtro de valores:
					self.array_filter.insert(0, self.output)
					self.array_filter.pop()

					if abs(self.array_filter[0] - self.array_filter[1]) < 15:
						self.output = self.output

					elif abs(self.array_filter[0] - self.array_filter[1] > 15) and abs(self.array_filter[0] - self.array_filter[2] < 10):
						self.output = self.output

					elif abs(self.array_filter[0] - self.array_filter[1]) > 15:
						self.output = self.last_output

				#print("<PID-ROLL> Output: ", self.output)
				self.kalman_window.insert(0, self.output)
				self.kalman_window.pop()
				kf = KalmanFilter(0,1)
				measurements = self.kalman_window
				self.output = kf.filter(measurements)[0][2]
				#print("<PID-ROLL> Kalman Output: ", self.output)

				self.output_pid.instance.set_number("Roll", self.output)
				self.output_pid.write()

				self.last_output = self.output
				first_loop = False
				#time.sleep(0.5)


if(__name__) == "__main__":
	print("<PID-ROLL> Inicio del programa")
	PIDRollClass = PID_Roll()
	PIDRollClass.update()
