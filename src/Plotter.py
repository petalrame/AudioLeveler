import matplotlib.pyplot as plt
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
from random import *
import numpy as np
import time

device = soundtouch_device('192.168.1.105')
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(100)
y = np.random.randn(100)
li, = ax.plot(x, y)
ax.relim() 
ax.autoscale_view(True,True,True)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
fig.canvas.draw()
plt.show(block=False)
while True:
    volume = device.volume()
    
    y[:-1] = y[1:]
    y[-1:] = float(volume.actual)
    li.set_ydata(y)
    fig.canvas.draw()
    time.sleep(0.01)



