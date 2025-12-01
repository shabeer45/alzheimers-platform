from flask import*

from database import*

patient=Blueprint('patient',__name__)


@patient.route ("/patienthome")
def patienthome():
    return render_template("patienthome.html")

