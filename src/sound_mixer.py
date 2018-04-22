"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import numpy as np
import time
import math


class VolumeController():
    """Controls the volume of the speaker"""
    def __init__(self, desired_vol=50):
        self.desired_audio_level = desired_vol
        self.duration = 5
        self.devices = discover_devices(timeout=2)  # Default timeout is 5 seconds
        self.total = 0
        self.max = 100
        self.num_iterations = 0
        self.min = 0
        self.sd_total = 0
        self.standard_deviation = 0


    def level_audio(self, indata, outdata, frames, time, status):
        # Run for the duration of the program
        for device in self.devices:
        #device = soundtouch_device('192.168.1.105')  # Manual configuration
        # Normalize the data coming in from the microphone to calculate the current level
            U, s, Vh = np.linalg.svd(indata, full_matrices=False) # The top s-value x 100 seems to be roughly the device volume
            ml_num = s[0]*100
            print("ML Num " + ml_num)
            volume_norm = np.linalg.norm(indata) * 100
            self.num_iterations = self.num_iterations + 1
            if volume_norm > self.max:
                self.max = volume_norm
            if volume_norm < self.min:
                self.min = volume_norm
            self.total = self.total + volume_norm
            avg = self.total / self.num_iterations
            sd_helper = pow((volume_norm - avg),2)
            self.sd_total += sd_helper
            self.standard_deviation = math.sqrt((self.sd_total / self.num_iterations))

            print("Max " + str(max))
            print("Min " + str(min))
            print("Avg" + str(avg))
            print("Standard deviation " + str(self.standard_deviation))
            scaled_value = ((100-0)/(self.max-self.min)) * (volume_norm - self.max) + 100
            print("Scaled value " + str(scaled_value))
            current_audio_level = int(scaled_value)
            print(int(current_audio_level))
            # Get each speakers current volume
            volume = device.volume()
            print("Device VOLUME: ", volume.actual)
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
        import sounddevice as sd
        while True:
            with sd.Stream(callback=self.level_audio):
                sd.sleep(self.duration * 1000)
        # TODO: Mechanism to stop loop above
