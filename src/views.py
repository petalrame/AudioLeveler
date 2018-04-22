import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sound_mixer import VolumeController

template_dir = os.path.abspath('../templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "asia4lyfe"

@app.route("/")
def index():
    return render_template(
        'index.html')

@app.route("/startControl", methods=["POST"])
def startControl():
    """ Starts volume control
    """
    volume = int(request.form["volumeSet"])
    if 'record' in session:
        print("Session Info: ", session)
        print("Volume control is already on. Doing nothing...")
    else:
        print("Setting session object")
        session["record"] = "ON"
        #handleVolControl(volume)
    return render_template(
        'index.html')

@app.route("/stopControl", methods=["POST"])
def stopControl():
    """ Stop volume control
    """
    if 'record' in session:
        session.pop('record', None)
        # TODO: Stop recording(AKA stop the never ending loop)
    else:
        print("Volume Control never even started!")
    return render_template(
        'index.html')

def handleVolControl(volume):
    controller = VolumeController(volume)
    controller.runner()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
