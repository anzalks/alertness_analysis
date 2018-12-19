# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:39:57 2018

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
    fig, ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('angular velocity', color=color)
    ax1.plot(f.time.dt.time, f.angular_vel, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.savefig(file_name +'.png')
    plt.close()
        
print("list of all files in the direcory")
print(file_list)

    
for file_name in file_list:
    plot_time_ang_vel (file_name)
