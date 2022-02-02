import rticonnextdds_connector as rti 
import threading 
import time 
import signal
#import psutil
import sys
import random
from pykalman import KalmanFilter

class PID_Pitch:

	def __init__(self):

		self.initializate_default_values()

		# DDS
		self.connector_suscriptor_attitude = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_radio = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_suscriptor_interfaz = rti.Connector(config_name="MyParticipantLibrary::ParticipanteSuscriptor", url="config.xml")
		self.connector_publicador = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml")	
		self.input_radio = self.connector_suscriptor_radio.get_input("Suscriptor::LectorRadio")
		self.input_attitude = self.connector_suscriptor_attitude.get_input("Suscriptor::LectorAttitude")
		self.output_pid = self.connector_publicador.get_output("Publicador::EscritorPID_pitch")
		self.input_interfaz = self.connector_suscriptor_interfaz.get_input("Suscriptor::LectorInterfaz")

	def getPitch_mando(self):
		
		while(True):

			# Esperamos por el dato PITCH del MANDO
			self.input_radio.wait()
			self.input_radio.take()

			# Guardamos el valor de PITCH-radio
			for sample in self.input_radio.samples.valid_data_iter:
				data = sample.get_dictionary()
				pitch_mando = data["Pitch"]
				#print("<PID-PITCH> Posicion recibida: ", pitch_mando)
		
			self.setPoint = pitch_mando

	def getPitch_attitude(self):

		while(True):

			# Esperamos por el dato PITCH del modulo AHRS
			self.input_attitude.wait()
			self.input_attitude.take()

			# Guardamos el valor de PITCH-AHRS
			for sample in self.input_attitude.samples.valid_data_iter:
				data = sample.get_dictionary()
				pitch_attitude = data["Pitch"]
				#print("<PID-PITCH> Posicion recibida Pitch-Attitude: ", pitch_attitude)
		
			self.feedbackValue = pitch_attitude
		

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
			print("<PID-PITCH> Esperando publicaciones de K")
			#self.input_interfaz.wait_for_publications()
			self.input_interfaz.wait()
			self.input_interfaz.take()

			for sample in self.input_interfaz.samples.valid_data_iter:
				data = sample.get_dictionary()
				if data["kp_pitch"] != 0:
					self.Kp = data["kp_pitch"]
				if data["kd_pitch"] != 0:
					self.Kd = data["kd_pitch"]
				if data["ki_pitch"] != 0:
					self.Ki = data["ki_pitch"]
				if data["wg_pitch"] != 0:
					self.windup_guard = data["wg_pitch"]

			print("<PID-PITCH> Actualizados valores de K")
			print("<PID-PITCH> self.kp: ",self.Kp)
			print("<PID-PITCH> self.kd: ",self.Kd)
			print("<PID-PITCH> self.ki: ",self.Ki)
			print("<PID-PITCH> self.windup_guard", self.windup_guard)


	def update(self):
		th = threading.Thread(target=self.update_const)
		th.daemon = True # Este hilo muere cuando el main finalize
		th.start()
		
		th1 = threading.Thread(target=self.getPitch_attitude)
		th1.daemon = True
		th1.start()

		th2 = threading.Thread(target=self.getPitch_mando)
		th2.daemon = True
		th2.start()

		first_loop = True
		continuar = False

		print("<PID-PITCH> Comenzamos el bucle de calculo del PID")
		while True:
			
			error = self.setPoint - self.feedbackValue
			self.current_time = time.time() * 1000
			self.last_time = self.current_time if self.last_time is None else self.last_time
			#print("<CURRENT_TIME>: ",self.current_time)
			# diferencia entre ahora y la ultima vez que hicimos calculos
			delta_time = self.current_time - self.last_time
			#print("<DELTA_TIME>: ",delta_time)
			# diferencia entre error de ahora con el anterior guardado
			delta_error = error - self.last_error

			# miramos si ha transcurrido el tiempo que hemos establecido como intervalo
			if(delta_time >= self.sample_time):

				# calculamos control proporcional
				self.Pterm = self.Kp * error
				#print("<PTERM>: ",self.Pterm)

				# calculo control integral
				self.Iterm += error * delta_time
				#print("<ITERM>: ",self.Iterm)
				# miramos si Iterm no esta por encima o por debajo del intervalo que consideremos como coherente
				if(self.Iterm < -self.windup_guard):
					self.Iterm = -self.windup_guard

				elif (self.Iterm > self.windup_guard):
					self.Iterm = self.windup_guard

				self.Dterm = 0.0

				if delta_time > 0:
					self.Dterm = delta_error / delta_time

				#print("<DTERM>: ",self.Dterm)
				# guardamos parametros para proximo caculo
				self.last_time = self.current_time
				self.last_error = error

				# hacemos calculo del PID
				self.output = self.Pterm + (self.Ki * self.Iterm) + (self.Kd * self.Dterm)

				#print("<PID-PITCH> Output: ",self.output)

				if first_loop == True:

					self.array_filter.insert(0,self.output)
					self.array_filter.pop()

				if first_loop == False:

					if self.output > 90:
						self.output = self.last_output
					elif self.output < -90:
						self.output = self.last_output

					# Filtro de valores

					self.array_filter.insert(0,self.output)
					self.array_filter.pop()

					if abs(self.array_filter[0] - self.array_filter[1]) < 15:
						self.output = self.output
					elif abs(self.array_filter[0] - self.array_filter[1] > 15) and abs(self.array_filter[0] - self.array_filter[2] < 10):
						self.output = self.output
					elif abs(self.array_filter[0] - self.array_filter[1]) > 15:
                                                self.output = self.last_output

				self.kalman_window.insert(0, self.output)
				self.kalman_window.pop()
				kf = KalmanFilter(0,1)
				measurements = self.kalman_window
				self.output = kf.filter(measurements)[0][2]
				#print("<PID-PITCH> Output:", self.output)
				self.output_pid.instance.set_number("Pitch", self.output)
				self.output_pid.write()

				self.last_output = self.output
				first_loop = False
				#print("RAM USAGE: ",psutil.virtual_memory()[2])
				#time.sleep(0.5)


if(__name__) == "__main__":

	print("<PID-PITCH> Inicio del programa")
	PIDPitchClass = PID_Pitch()
	PIDPitchClass.update()

