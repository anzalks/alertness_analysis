#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 12:04:40 2019

@author: anzal
"""
import os #imported the Os library 
import pandas as pd #imported pandas library as pd
import matplotlib.pyplot as plt #imported matplotlib library as plt
import numpy as np #imported numpy library as np
import tkinter as tk

def Set_wd():
    from tkinter.filedialog import askdirectory
    root = tk.Tk()
    root.withdraw()
    x = askdirectory()    
    os.chdir(x)
    Set_wd.x=x

Set_wd()

    
dirname = Set_wd.x

dirname = '/Users/anzal/Downloads/calib_vel/calib_vel_M_1/'

datFs = []
for d, ds, fs in os.walk(dirname):
    for f in fs:
        if '.dat' in f:
            fp = os.path.join(d, f)
            datFs.append(fp)
            

txtFs = []
for d, ds, fs in os.walk(dirname):
    for f in fs:
        if '.txt' in f:
            fp = os.path.join(d, f)
            txtFs.append(fp)

file_name = datFs

hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
rd= pd.read_csv(file_name, names=hn,)
rd['time'] = pd.to_datetime(rd['timestamp_arduino'])  
tc=rd[rd.angular_vel > 0].index.values[0]
h=rd[rd.index > tc]
ec=h[h.angular_vel <=0].index.values[0]
f=h[h.index < ec]
f=pd.DataFrame.reset_index(f)
f['velocity'] = f.angular_vel*7.5

tms_f = f['time'].dt.second + f['time'].dt.microsecond /1000000

plt.plot(tms_f,f.velocity)

vel_diff = pd.DataFrame.diff(abs(f.velocity))
time_diff = pd.DataFrame.diff(tms_f)
acc = vel_diff/time_diff

plt.plot(tms_f,acc)

plt.plot(tms_f,f.angular_vel)


fn_txt = '/Users/anzal/Downloads/calib_vel/calib_vel_M_1/name=calib_vel_st=M_sn=1trial=0.txt'
txtFs
hl= ["time"]
tf= pd.read_csv(fn_txt, names=hl)
vel_str = 690/tf