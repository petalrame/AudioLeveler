"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import sounddevice as sd
import numpy as np
import time
import math

total = 0
max = 100
num_iterations = 0
min = 0
sd_total = 0
standard_deviation = 0
class VolumeController():
    """Controls the volume of the speaker"""
    def __init__(self, desired_vol=50):
        self.desired_audio_level = desired_vol
        self.duration = 5
        self.devices = discover_devices(timeout=2)  # Default timeout is 5 seconds


    def level_audio(self, indata, outdata, frames, time, status):
        # Run for the duration of the program
        global total
        global max
        global num_iterations
        global min
        global sd_total
        global standard_deviation

        #for device in self.devices:
        device = soundtouch_device('192.168.1.105')  # Manual configuration
        # Normalize the data coming in from the microphone to calculate the current level
        volume_norm = np.linalg.norm(indata) * 100
        num_iterations = num_iterations + 1
        if volume_norm > max:
            max = volume_norm
        if volume_norm < min:
            min = volume_norm
        total = total + volume_norm
        avg = total / num_iterations
        sd_helper = pow((volume_norm - avg),2)
        sd_total += sd_helper
        standard_deviation = math.sqrt((sd_total / num_iterations))

        print("Max " + str(max))
        print("Min " + str(min))
        print("Avg" + str(avg))
        print("Standard deviation " + str(standard_deviation))
        scaled_value = ((100-0)/(max-min)) * (volume_norm - max) + 100
        print("Scaled value " + str(scaled_value))
        current_audio_level = int(scaled_value)
        print(int(current_audio_level))
        # Get each speakers current volume
        volume = device.volume()
        if current_audio_level < self.desired_audio_level:
            # Something sketchy happens where the audio comes in at 0
            if current_audio_level is not 0:
                print("INCREASING VOLUME")
                device.set_volume(volume.actual + 1)
        elif current_audio_level > self.desired_audio_level:
            print("DECREASING VOLUME")
            device.set_volume(volume.actual - 1)
        else:
            # relax for 5 seconds if the sound level is good
            print("Sound is good!")


    def runner(self):
        print("Running...")
        print("Desired: " + str(self.desired_audio_level))
        while True:
            with sd.Stream(callback=self.level_audio):
                sd.sleep(self.duration * 1000)
        # TODO: Mechanism to stop loop above
