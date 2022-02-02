import time
import navio.ms5611
import navio.util
import spidev
import sys
import navio.mpu9250
import math
import rticonnextdds_connector as rti
from estimator.YawEstimator import comp_filt
#import threading
from pykalman import KalmanFilter
import numpy as np

import sys, getopt
sys.path.append('.')
import RTIMU
import os.path

###########################

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

if (not pressure.pressureInit()):
    print("Pressure sensor Init Failed")
else:
    print("Pressure sensor Init Succeeded")

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

############################

#navio.util.check_apm()

baro = navio.ms5611.MS5611()
baro.initialize()

altura = 0

def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));


def main():

	connector = rti.Connector(config_name="MyParticipantLibrary::ParticipantePublicador", url="config.xml")
	output = connector.get_output("Publicador::EscritorAttitude")

	last_pitch = 0
	last_roll = 0
	last_yaw = 0
	first_loop = True
	offset_yaw = 0

	altura = 0

	kalman_window_yaw = [0,0,0]
	kalman_window_pitch = [0,0,0]
	kalman_window_roll = [0,0,0]

	while (True):

		## RTIMULIB

		if imu.IMURead():

			data = imu.getIMUData()
			#(data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
			fusionPose = data["fusionPose"]
			#print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
			roll = math.degrees(fusionPose[0])
			pitch = math.degrees(fusionPose[1])
			yaw = math.degrees(fusionPose[2])

			#if (data["pressureValid"]):
			#	print("Pressure: %f, height above sea level:" % (data["pressure"]))
				#altura = computeHeight(data["pressure"])
			
			#if (data["temperatureValid"]):
        		#	print("Temperature: %f" % (data["temperature"]))


			if first_loop == True:
				offset_yaw = yaw

			# Offset > 0
			if(yaw > 0 and offset_yaw > 0):
				if(yaw > offset_yaw):
					yaw = yaw - offset_yaw
				elif(yaw < offset_yaw):
					yaw = 0 - (offset_yaw - yaw)

			elif(yaw < 0 and offset_yaw > 0):
                                yaw = 0 - (abs(offset_yaw) + abs(yaw))

			# Offset < 0
			elif(yaw < 0 and offset_yaw < 0):
				if(yaw > offset_yaw):
					yaw = 0 + (abs(yaw) - abs(offset_yaw)) # +
				elif(yaw < offset_yaw):
					yaw = 0 - (abs(offset_yaw) - abs(yaw))

			elif(yaw > 0 and offset_yaw < 0):
				yaw = 0 + abs(offset_yaw) + yaw

			if(yaw > 180):
				yaw = -180 + (yaw - 180)
			if(yaw < -180):
				yaw = 180 - (abs(yaw) - 180)

			yaw = (((yaw  - (-180)) * (90 - (-90))) / (180 - (-180))) + (-90)

			#print("r: %f p: %f y: %f" % (roll,pitch,yaw))

			output.instance.set_number("Altura",altura)
			output.instance.set_number("Pitch",pitch)
			output.instance.set_number("Roll",roll)
			output.instance.set_number("Yaw",yaw)
			output.write()

			time.sleep(poll_interval*1.0/1000.0)

			first_loop = False
		###########################################################################################

		

if(__name__) == "__main__":

	main()
	print("Saliendo del programa principal...")
