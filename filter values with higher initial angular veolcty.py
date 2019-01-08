#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 12:34:52 2019

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
dirname = '/Users/anzal/Downloads/Calibration_data/Calibration_data_M_1/data/'

Ang_vel_thres = -0.1

def collect_values(file_name, ax = None):
    hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    rd= pd.read_csv(file_name, names=hn,)
    rd['time'] = pd.to_datetime(rd['timestamp_arduino'])  
    g=min(rd.angular_vel)
    tc=rd[rd.angular_vel==g].index.values[0]
    h=rd[rd.index < tc]
    f=h[h.angular_vel < 0]
    f=pd.DataFrame.reset_index(f)

    if ax:    
        ax.plot(abs(f.encoder_val), abs(f.angular_vel))
    return f

f_list_all = []
for file in os.listdir(dirname):
    if file.endswith(".dat"):
        f_list_all.append(os.path.join(dirname, file))
        
file_list = []

for file in f_list_all:
    header_name=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    df_fl= pd.read_csv(file, names = header_name,)
    df_fl['time'] = pd.to_datetime(df_fl['timestamp_arduino'])  
    g_fl=min(df_fl.angular_vel)
    n=df_fl[df_fl.angular_vel==g_fl].index.values[0]
    o=df_fl[df_fl.index < n]
    if (o.angular_vel[0:1] > Ang_vel_thres).bool():
       file_list.append(file)        

    
conc_list = []
plt.figure()
ax = plt.subplot(111)
for file_name in file_list:
    if len(collect_values(file_name, ax)) == 0:
        continue
    else:
        conc_list.append(collect_values(file_name, ax))
ax.legend(['Angular velocity'], loc=1)
plt.savefig( 'angular_vel_vs_encoder_val_raw.png' )
plt.close(fig) 
    
final_df = pd.concat(conc_list)
final_df = final_df.sort_values(by='encoder_val', ascending=False)
w=abs(final_df.encoder_val*(6.28/2400))# encoder value*(2pi/2400) instantanious angle value
ang_vel = abs(final_df.angular_vel)

area = 10
colors = ang_vel
l="angl_vel_vs_ang_disp"
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.set_rlabel_position(-20)
c = ax.scatter(ang_vel, w,  c=colors, s=area, cmap='viridis', alpha=0.75)
plt.colorbar(c)
area1 = 3
c1 = ax.scatter(w, w, c='black', s= area1, alpha=0.75 )
ax.legend(['Angular velocity', 'encoder disk position'], loc=1)
plt.savefig( 'polar_angular_vel_vs_encoder_val_raw.png')



for (root,dirs,files) in os.walk('dirname', topdown=True):
    f_list_all = []
    for f in f_list_all:
        f_list_all.append(os.path.join(dirs, files))
    
for d_names,f_names in os.walk(dirname):
	for f in f_list_all:
		f_list_all.append(os.path.join(d_names, f))