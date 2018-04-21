"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import sounddevice as sd
import numpy as np
import time

class VolumeController():
    """ Controls the volume of the speaker
    """
    def __init__(self, desired_vol=50):
        self.desired_audio_level = desired_vol
        self.duration = 5
        self.devices = discover_devices(timeout=2)  # Default timeout is 5 seconds

    def level_audio(self, indata, outdata, frames, time, status):
        # Run for the duration of the program
        for device in self.devices:
            # Normalize the data coming in from the microphone to calculate the current level
            volume_norm = np.linalg.norm(indata) * 100
            current_audio_level = int((int(volume_norm) / 150) * 100)
            if current_audio_level <= 0:
                continue
            print("|" * int(current_audio_level))
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
                time.sleep(5)


    def runner(self):
        print("Running...")
        print("Desired: " + str(self.desired_audio_level))
        while True:
            with sd.Stream(callback=self.level_audio):
                sd.sleep(self.duration * 1000)
        # TODO: Mechanism to stop loop above
