#!/bin/bash

python Attitude.py &
python Radio.py &
python3 PID-pitch.py &
python3 PID-roll.py &
python3 PID-yaw.py &
python Mixer.py &
python Motor.py &

wait

