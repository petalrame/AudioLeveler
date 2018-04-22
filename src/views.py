import os
from flask import Flask, flash, redirect, render_template, request, session, abort
import signal, psutil
from sound_mixer import VolumeController

template_dir = os.path.abspath('../templates')
static_dir = os.path.abspath('../static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
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

        # Create child proc for vol control
        n = os.fork()

        # n > 0 is parent 
        if n == 0:
            handleVolControl(volume)
            #plotter()
        elif n > 0:
            parent = psutil.Process(os.getpid())
            children = parent.children()
            session["PID"] = str(children[-1].pid)
        else:
            print("There was an error")
    return render_template(
        'index.html')

@app.route("/stopControl", methods=["POST"])
def stopControl():
    """ Stop volume control
    """
    if 'record' in session:
        print("Stopping PID: ", session["PID"])
        session.pop('record', None)
        os.kill(int(session["PID"]), signal.SIGTERM)
        session.pop('PID', None)
    else:
        print("Volume Control never even started!")
    return render_template(
        'index.html', plot_url="../static/img_disp")

def handleVolControl(volume):
    controller = VolumeController(volume)
    controller.runner()



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='174.225.10.150', port=port)
