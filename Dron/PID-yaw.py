import rticonnextdds_connector as rti
import threading
import time
from pykalman import KalmanFilter

class PID_Yaw:

	def __init__(self):

		self.initializate_default_values()

		# DDS
		self.connector_suscriptor_attitude = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_radio = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_interfaz = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_publicador = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml")	
		self.input_radio = self.connector_suscriptor_attitude.get_input("Suscriptor::LectorRadio")
		self.input_attitude = self.connector_suscriptor_radio.get_input("Suscriptor::LectorAttitude")
		self.output_pid = self.connector_publicador.get_output("Publicador::EscritorPID_yaw")
		self.input_interfaz = self.connector_suscriptor_interfaz.get_input("Suscriptor::LectorInterfaz")

	def getYaw_mando(self):
		
		while(True):
			# Esperamos por el dato YAW del MANDO
			self.input_radio.wait()
			self.input_radio.take()

			# Guardamos el valor de YAW-radio
			for sample in self.input_radio.samples.valid_data_iter:
				data = sample.get_dictionary()
				yaw_mando = data["Yaw"]
				#print("<PID-YAW> Posicion recibida: ", yaw_mando)

			self.setPoint = yaw_mando

	def getYaw_attitude(self):

		while(True):
			# Esperamos por el dato YAW del modulo AHRS
			self.input_attitude.wait()
			self.input_attitude.take()

			# Guardamos el valor de YAW-AHRS
			for sample in self.input_attitude.samples.valid_data_iter:
				data = sample.get_dictionary()
				yaw_attitude = data["Yaw"]
				#print("<PID-YAW> Posicion recibida Attitude: ", yaw_attitude)
			
			self.feedbackValue = yaw_attitude


	def initializate_default_values(self):
		
		# reiniciamos variables
		self.Kp = 0.3
		self.Ki = 0.6
		self.Kd = 0.3
		self.Pterm = 0.00
		self.Iterm = 0.00
		self.Dterm = 0.00
		self.sample_time = 4
		self.current_time = None
		self.last_time = None
		self.last_error = 0.00
		self.last_output = 0
		self.windup_guard = 2
		self.array_filter = [0,0,0]
		self.kalman_window = [0,0,0]
		self.setPoint = 0.00
		self.feedbackValue = 0.00

	def update_const(self):

		while True:
			print("<PID-YAW> Esperando publicaciones de K")
			#self.input_interfaz.wait_for_publications()
			self.input_interfaz.wait()
			self.input_interfaz.take()

			for sample in self.input_interfaz.samples.valid_data_iter:
				data = sample.get_dictionary()
				if data["kp_yaw"] != 0:
					self.Kp = data["kp_yaw"]
				if data["kd_yaw"] != 0:
					self.Kd = data["kd_yaw"]
				if data["ki_yaw"] != 0:
					self.Ki = data["ki_yaw"]
				if data["wg_yaw"] != 0:
					self.windup_guard = data["wg_yaw"]

			print("<PID-YAW> Actualizados valores de K")
			print("<PID-YAW> self.kp: ",self.Kp)
			print("<PID-YAW> self.kd: ",self.Kd)
			print("<PID-YAW> self.ki: ",self.Ki)
			print("<PID-YAW> self.windup_guard: ", self.windup_guard)

	def update(self):

		th = threading.Thread(target=self.update_const)
		th.daemon = True # Este hilo muere cuando el main finalize
		th.start()

		th1 = threading.Thread(target=self.getYaw_attitude)
		th1.daemon = True
		th1.start()

		th2 = threading.Thread(target=self.getYaw_mando)
		th2.daemon = True
		th2.start()

		first_loop = True

		print("<PID-YAW> Comenzamos el bucle de calculo del PID")

		while True:

			# Conseguimos los valores del yaw de mando y del modulo AHRS y calculamos el error
			error = self.setPoint - self.feedbackValue

			self.current_time = time.time() * 1000
			self.last_time = self.current_time if self.last_time is None else self.last_time

			# diferencia entre ahora y la ultima vez que hicimos calculos
			delta_time = self.current_time - self.last_time
			#print("<DELTA_TIME>: ",delta_time)
			# diferencia entre error de ahora con el anterior guardado
			delta_error = error - self.last_error
			#print("<DELTA_ERROR>: ",delta_error)
			# miramos si ha transcurrido el tiempo que hemos establecido como intervalo
			if(delta_time >= self.sample_time):

				# calculamos control proporcional
				self.PTerm = self.Kp * error

				# calculo control integral
				self.Iterm += error * delta_time
				#print("<ERROR*DELTA_TIME>: ",(error*delta_time))
				#print("<ITERM>: ",self.Iterm)
				# miramos si Iterm no esta por encima o por debajo del intervalo que consideremos como coherente
				if(self.Iterm < -self.windup_guard):
					self.Iterm = -self.windup_guard

				elif (self.Iterm > self.windup_guard):
					self.Iterm = self.windup_guard

				self.DTerm = 0.0

				if delta_time > 0:
					self.DTerm = delta_error / delta_time

					self.kalman_window.insert(0,self.DTerm)
					self.kalman_window.pop()
					kf = KalmanFilter(0,1)
					measurements = self.kalman_window
					self.DTerm = kf.filter(measurements)[0][2]
					#print("<DTerm> ",self.DTerm)

				# guardamos parametros para proximo caculo
				self.last_time = self.current_time
				self.last_error = error

				# hacemos calculo del PID
				self.output = self.PTerm + (self.Ki * self.Iterm) + (self.Kd * self.DTerm)
				#print("<PID-YAW> Output before filter: ", self.output)

				
				self.output_pid.instance.set_number("Yaw", self.output)
				self.output_pid.write()

				self.last_output = self.output
				first_loop = False

				#time.sleep(0.5)

if(__name__) == "__main__":
	print("<PID-YAW> Inicio del programa")
	PIDYawClass = PID_Yaw()
	PIDYawClass.update()
