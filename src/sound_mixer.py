"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import sounddevice as sd
import numpy as np
devices = discover_devices(timeout=2)  # Default timeout is 5 seconds

# Sound level we want to stay at
DESIRED_AUDIO_LEVEL = 50

#
current_audio_level = 0

# Record indefinately
duration = 50


def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    current_audio_level = volume_norm
    print(int(volume_norm) * "|")


def level_audio():
    # Run for the duration of the program
    while True:
        for device in devices:
            # Get each speakers current volume
            volume = device.volume()
            if current_audio_level < DESIRED_AUDIO_LEVEL:
                device.set_volume(volume.actual + 5)
            elif current_audio_level > DESIRED_AUDIO_LEVEL:
                device.set_volume(volume.actual - 5)


if __name__ == '__main__':
    with sd.Stream(callback=print_sound):
        sd.sleep(duration * 1000)
        level_audio
