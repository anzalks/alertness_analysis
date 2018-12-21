# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:29:45 2018

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

def plot_time_ang_vel(file_name):
    hn=["timestamp_arduino", "trial_count_", "puff", "tone", "led", "camera","microscope","something_else", "trial_state_","encoder_val","angular_vel"] #made an array with header names
    rd= pd.read_csv(file_name, names=hn,)
    rd['time'] = pd.to_datetime(rd['timestamp_arduino'])
    g=min(rd.angular_vel)
    tc=rd[rd.angular_vel==g].index.values[0]
    h=rd[rd.index < tc]
    f=h[h.angular_vel < 0]
    dif_tim = pd.DataFrame.diff(f.time)
    t = ((dif_tim.dt.microseconds) * (f.angular_vel))/1000000
    t=t.astype(float)
    t = pd.DataFrame(t, columns=['ang_disp'])
    t = abs(t)
    ang_vel = abs(f.angular_vel)
    
    fig, ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('angular velocity', color=color)
    ax1.plot(f.time.dt.time, f.angular_vel, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend()
    plt.savefig(file_name +'.png')
    plt.close()
    
    j="angl_vel_vs_time"
    fig, ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('angular displacement')
    ax1.set_ylabel('angular velocity', color=color)
    ax1.plot(t.ang_disp,ang_vel, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend()
    plt.savefig(file_name +"_"+j +"_"+'.png')
    plt.close()
    
    area = 50
    colors = ang_vel
    l="angl_vel_vs_ang_disp"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.set_rlabel_position(-45)
    c = ax.scatter(ang_vel, t.ang_disp,  c=colors, s=area, cmap='hsv', alpha=0.75)
    ax.set_title("angular velocity v/s angular displacement", va='bottom')
    ax.legend()
    plt.savefig(file_name +"_"+l+"_"+'.png')
    plt.close()

for file_name in file_list:
    plot_time_ang_vel (file_name)
    print(file_name)