#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 11:31:24 2018

@author: anzalks
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

file_list = []
for file in os.listdir(dirname):
    if file.endswith(".dat"):
        file_list.append(os.path.join(dirname, file))


def collect_values(file_name, ax = None):
    hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    rd= pd.read_csv(file_name, names=hn,)
    rd['time'] = pd.to_datetime(rd['timestamp_arduino'])  
    g=min(rd.angular_vel)
    tc=rd[rd.angular_vel==g].index.values[0]
    h=rd[rd.index < tc]
    f=h[h.angular_vel < 0]
#    m=pd.DataFrame({'angular_vel':f.angular_vel-f['angular_vel'].iloc[0]})
#    m=pd.DataFrame(m).transpose()
#    f= f.loc[f['angular_vel'], 'angular_vel'] = m
    f=pd.DataFrame.reset_index(f)
    if ax:    
        ax.plot(abs(f.encoder_val), abs(f.angular_vel))
    return f
    
conc_list = []
plt.figure()
ax = plt.subplot(111)
for file_name in file_list:
    conc_list.append(collect_values(file_name, ax))
plt.savefig( 'angular_vel_vs_encoder_val_raw.png' )
    
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
