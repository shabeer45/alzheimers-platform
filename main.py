from flask import *
from public import public
from admin import admin
from user import user
from Doctor import Doctor
from patient import patient
from api import api

app=Flask(__name__)


app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(Doctor)
app.register_blueprint( patient)
app.register_blueprint(api)

app.secret_key='secret_key'

if __name__ == "__main__":
    app.run()


