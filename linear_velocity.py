#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 16:21:15 2019

@author: anzal
"""
import os #imported the Os library 
import pandas as pd #imported pandas library as pd
import matplotlib.pyplot as plt #imported matplotlib library as plt
import numpy as np #imported numpy library as np
import tkinter as tk
#
#def Set_wd():
#    from tkinter.filedialog import askdirectory
#    root = tk.Tk()
#    root.withdraw()
#    x = askdirectory()    
#    os.chdir(x)
#    Set_wd.x=x
#
#Set_wd()
#
#    
#dirname = Set_wd.x
#
dirname = '/Users/anzal/Downloads/calib_vel/calib_vel_M_1/'

os.chdir('/Users/anzal/Downloads/calib_vel/')

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


def rot_vel(datFs, ax = None):
    hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    rd= pd.read_csv(datFs, names=hn,)
    rd['time'] = pd.to_datetime(rd['timestamp_arduino'])  
    tc=rd[rd.angular_vel > 0].index.values[0]
    h=rd[rd.index > tc]
    ec=h[h.angular_vel <=0].index.values[0]
    f=h[h.index < ec]
    f=pd.DataFrame.reset_index(f)
    f['velocity'] = f.angular_vel*7.5
    tms_f = f['time'].dt.second + f['time'].dt.microsecond /1000000
    if ax:    
        ax.plot(tms_f,f.velocity)
    return (f)

def rot_vel_av(datFs):
    hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    rd= pd.read_csv(datFs, names=hn,)
    rd['time'] = pd.to_datetime(rd['timestamp_arduino'])  
    tc=rd[rd.angular_vel > 0].index.values[0]
    h=rd[rd.index > tc]
    ec=h[h.angular_vel <=0].index.values[0]
    f=h[h.index < ec]
    f=pd.DataFrame.reset_index(f)
    f['velocity'] = f.angular_vel*7.5
    m_vel = pd.DataFrame({'mean':f.velocity.describe()['mean']},index=[0])
    return (m_vel)

def str_vel(txtFs, ax = None):
    hl= ["time"]
    tf= pd.read_csv(txtFs, names=hl)
    vel_str = 690/tf
    return vel_str

    
conc_list_dat = []
plt.figure()
ax = plt.subplot(111)
for fl_n in datFs:
    conc_list_dat.append(rot_vel(fl_n, ax))
conc_list_dat = pd.concat(conc_list_dat)
ax.set_xlabel("time (s)")
ax.set_ylabel("Angular velocity (rad/s)")
plt.savefig('raw_plot_ang_vel(rad per s)_vs_time(s).png')
plt.show()
plt.close()


conc_list_dat_vel = []
for fl_n in datFs:
    conc_list_dat_vel.append(rot_vel_av(fl_n))
conc_list_dat_vel = pd.concat(conc_list_dat_vel)
conc_list_dat_vel = pd.DataFrame.reset_index(conc_list_dat_vel)
conc_list_dat_vel = conc_list_dat_vel.fillna(0)
    
conc_list_txt = []
for fl_n in txtFs:
    conc_list_txt.append(str_vel(fl_n, ax))
conc_list_txt = pd.concat(conc_list_txt)
conc_list_txt = pd.DataFrame.reset_index(conc_list_txt)
conc_list_txt = conc_list_txt.fillna(0)

vel_comp = pd.DataFrame({'velocity_from_rotary_encoder':conc_list_dat_vel['mean'],'velocity_external':conc_list_txt['time']})
vel_comp = vel_comp.fillna(0)
vel_comp = vel_comp[(vel_comp != 0).all(1)]
vel_comp = vel_comp[(vel_comp > 5).all(1)]
vel_comp = pd.DataFrame.reset_index(vel_comp)
vel_comp['difference_in_vel'] = abs(vel_comp.velocity_from_rotary_encoder - vel_comp.velocity_external)

plt.figure()
ax = plt.subplot(111)
ax.bar(vel_comp.index-0.2, vel_comp.velocity_from_rotary_encoder,width=0.5,color='red',align='center')
ax.bar(vel_comp.index +0.2, vel_comp.velocity_external,width=0.5,color='blue',align='center')
ax.set_xlabel("trial no.s")
ax.set_ylabel("linear velocity (cm/s)")
ax.legend(['velocity obtained from rotary encoder', 'velocity obtained using external timer'], loc=1)
plt.savefig("velocity(cm_per_s)_vs_trial_nos.png")
plt.show()
plt.close()

plt.figure()
ax = plt.subplot(111)
ax.bar(vel_comp.index-0.2, vel_comp.difference_in_vel,width=0.5,color='black',align='center')
ax.set_xlabel("trial no.s")
ax.set_ylabel("lin vel diff in cm")
ax.legend(['difference in velocity from different sources'], loc=1)
plt.savefig('velocity_difference(cm_per_s)_vs_trial_no.png')
plt.show()
plt.close()
