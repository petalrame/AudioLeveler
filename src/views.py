import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sound_mixer import VolumeController

template_dir = os.path.abspath('../templates')

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def index():
    return render_template(
        'index.html')

@app.route("/", methods=["POST"])
def startControl():
    volume = int(request.form["volumeSet"])
    if 'Record' in session:
        print("Volume control is already on")
    else:
        session["Record"] = "ON"
        handleVolControl(volume)
    return

@app.route("/", methods=["POST"])
def stopControl():
    if 'Record' in session:
        # Stop recording(AKA stop the never ending loop)
    else:
        print("Volume Control never even started!")

def handleVolControl(volume):
    controller = VolumeController(volume)
    controller.runner()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
