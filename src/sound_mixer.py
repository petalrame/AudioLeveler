"""Contains Bose API Code"""
from libsoundtouch import soundtouch_device, discover_devices
from libsoundtouch.utils import Source, Type
import sounddevice as sd
import numpy as np
devices = discover_devices(timeout=2)  # Default timeout is 5 seconds

# Sound level we want to stay at
DESIRED_AUDIO_LEVEL = 18

#

# Record indefinately
duration = 1


def level_audio(indata, outdata, frames, time, status):
    # Run for the duration of the program
    for device in devices:
        volume_norm = np.linalg.norm(indata) * 100
        current_audio_level = int(volume_norm)
        print(current_audio_level * "|")
        # Get each speakers current volume
        volume = device.volume()
        if current_audio_level < DESIRED_AUDIO_LEVEL:
            print("INCREASING VOLUME")
            device.set_volume(volume.actual + 5)
        elif current_audio_level > DESIRED_AUDIO_LEVEL:
            print("DECREASING VOLUME")
            device.set_volume(volume.actual - 5)
        else:
            print("Volume is good!")


main(audio_level):
    DESIRED_AUDIO_LEVEL = audio_level
    while True:
        with sd.Stream(callback=level_audio):
            sd.sleep(duration * 1000)


if __name__ == '__main__':
    main()
