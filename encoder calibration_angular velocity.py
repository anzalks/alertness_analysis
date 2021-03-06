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
    w=abs(f.encoder_val*(6.28/2400))# encoder value*(2pi/2400) instantanious angle value
    ang_vel = abs(f.angular_vel)
    
    fig, ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('angular velocity (rad/s)', color=color)
    ax1.plot(f.time.dt.time, abs(f.angular_vel), color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend()
    plt.savefig(file_name +'.png')
    plt.close()
    
    j="angl_vel_vs_time"
    fig, ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('angular displacement (rad)')
    ax1.set_ylabel('angular velocity (rad/s)', color=color)
    ax1.plot(w,ang_vel, color=color)
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
    c = ax.scatter(ang_vel, w,  c=colors, s=area, cmap='hsv', alpha=0.75)
    ax.set_title("angular velocity v/s angular displacement", va='bottom')
    ax.legend()
    plt.colorbar(c)
    plt.savefig(file_name +"_"+l+"_"+'.png')
    plt.close()

for file_name in file_list:
    plot_time_ang_vel (file_name)
    print(file_name)