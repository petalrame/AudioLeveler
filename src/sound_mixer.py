"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import sounddevice as sd
import numpy as np

class VolumeController():
    """ Controls the volume of the speaker
    """
    def __init__(self, desired_vol=50):
        self.desired_audio_level = desired_vol
        self.duration = 10
        self.devices = discover_devices(timeout=2)  # Default timeout is 5 seconds

    def level_audio(self, indata, outdata, frames, time, status):
        # Run for the duration of the program
        for device in self.devices:
            print("indata: ", indata)
            volume_norm = np.linalg.norm(indata) * 100
            print("vol_norm: ", volume_norm)
            current_audio_level = int(volume_norm)
            print(current_audio_level * "|")
            # Get each speakers current volume
            volume = device.volume()
            if current_audio_level < self.desired_audio_level:
                print("INCREASING VOLUME")
                device.set_volume(volume.actual + 5)
            elif current_audio_level > self.desired_audio_level:
                print("DECREASING VOLUME")
                device.set_volume(volume.actual - 5)
            else:
                print("Volume is good!")


    def runner(self):
        print("Running...")
        while True:
            with sd.Stream(callback=self.level_audio):
                sd.sleep(self.duration * 1000)
        print("Process Terminated.")
        # TODO: Mechanism to stop loop above
