# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:39:57 2018

@author: anzalks
"""

import os #imported the Os library 
import pandas as pd #imported pandas library as pd
import matplotlib.pyplot as plt #imported matplotlib library as plt
import numpy as np #imported numpy library as np
os.chdir("/home/anzalks/DATA/Calibration_data/Calibration_data_M_1/2018-12-14T17:01:32.948658/")
hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
rd= pd.read_csv('name=Calibration_data_st=M_sn=1trial=0.dat', names=hn,)
rd['time'] = pd.to_datetime(rd['timestamp_arduino'])
fig, ax1 = plt.subplots()
color = 'red'
ax1.set_xlabel('time')
ax1.set_ylabel('angular velocity', color=color)
ax1.plot(rd.time.dt.time, rd['angular_vel'], color=color)
ax1.tick_params(axis='y', labelcolor=color)