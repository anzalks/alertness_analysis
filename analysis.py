# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#run the analyze_trial_video.py in Mousebehaviour/analysis repository in github on any tiff file and obdain the dat file. 
#open thus obtained dat file as raw data.
import os #imported the Os library 
import pandas as pd #imported pandas library as pd
import matplotlib.pyplot as plt #imported matplotlib library as plt
import numpy as np #imported numpy library as np
import Tkinter, tkFileDialog
root = Tkinter.Tk()
root.withdraw()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
os.chdir(dirname) #changd the workingdirectory to the file path

file_list = []
for file in os.listdir(dirname):
    if file.endswith(".dat"):
        file_list.append(os.path.join(dirname, file))
print(file_list)
    
hn=["timestamp_camera","timestamp_arduino","frame_no", "trial_count_", "puff", "tone", "led", "motion1", "motion2", "camera", "microscope", "trial_state_","Eye_pixel"] #made an array with header names
rd= pd.read_csv(file_list, names=hn) #import CSV as variable rd, with the header as hn
rd = rd.dropna() #to remove all the rows with NAs
rd= rd.applymap(lambda x: x.replace("['","")) #removed different things
rd= rd.applymap(lambda x: x.replace("']",""))
rd= rd.applymap(lambda x: x.replace("'",""))
nd=rd[['frame_no', 'trial_count_', 'puff', 'tone', 'led', 'motion1', 'motion2', 'camera', 'microscope','Eye_pixel']]
cols = nd.columns[nd.dtypes.eq(object)]
nd[cols] = nd[cols].apply(pd.to_numeric, errors='coerce', axis=0)
rd['time'] = pd.to_datetime(rd['timestamp_arduino']) #converted the string to timestamp
fd = pd.concat([nd, rd['time']], axis=1)# concactenated the  two matrices

#rd.set_index('timestamp', inplace=True) #sets timestamp as the index, applicable to any column header, eg:trial_state_.
#rd.reset_index(inplace=True) (-to reset index)
#rd.plot(kind='scatter',x='time',y='trial_count_', color='red',linewidth=5) -plots timestamp v/s trial count
# row, columns = rd.shape 
#'rows' -will give the length of rows and 'columns' will give the length of columns

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time')
ax1.set_ylabel('eye state', color=color)
ax1.plot(fd.time.dt.time, fd['Eye_pixel'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax3 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('state', color=color)  # we already handled the x-label with ax1
ax2.plot(fd.time.dt.time, fd['led'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

color = 'tab:green'
ax3.set_ylabel('', color=color)  # we already handled the x-label with ax1
ax3.plot(fd.time.dt.time, fd['puff'], color=color)
ax3.tick_params(axis='y', labelcolor=color)


fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()