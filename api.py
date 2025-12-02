import os
from flask import *
from face_model import *
from facedetection import *
from database import *
from datetime import datetime

api = Blueprint('api', __name__)


# ------------------- REGISTER ----------------------
@api.route('/reg')
def reg():
    data = {}
    fname = request.args['fname']
    lname = request.args['lname']
    email = request.args['email']
    phone = request.args['phone']
    place = request.args['place']
    gender = request.args['gender']
    username = request.args['username']
    password = request.args['password']

    print(fname, lname, email, phone, place, gender, username, password)

    a = "insert into login values(null,'%s','%s','caretaker')" % (username, password)
    b = insert(a)

    c = "insert into caretaker values(null,'%s','%s','%s','%s','%s','%s','%s')" % (
        b, fname, lname, email, phone, gender, place
    )

    res = insert(c)
    if res:
        data['status'] = 'success'
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- LOGIN (FIXED) ----------------------
@api.route('/log', methods=['POST'])
def log():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return {"status": "failed", "message": "No input"}

        qry = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (username, password)
        res = select(qry)

        if res:
            return {"status": "success", "data": res}
        else:
            return {"status": "failed", "message": "Invalid credentials"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

        # CARETAKER CHECK
        a = "SELECT * FROM login INNER JOIN caretaker ON login.loginid = caretaker.login_id WHERE username='%s' AND password='%s'" % (username, password)
        res = select(a)

        if res:
            data['status'] = 'success'
            data['view'] = res
            return jsonify(data)

        # PATIENT CHECK
        b = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (username, password)
        x = select(b)

        if x:
            data['status'] = 'patient'
            data['view'] = x
            return jsonify(data)

        # INVALID USER
        data['status'] = 'failed'
        data['message'] = 'Invalid username or password'
        return jsonify(data)

    except Exception as e:
        print("LOGIN ERROR:", e)
        data['status'] = 'error'
        data['message'] = str(e)
        return jsonify(data)


# ------------------- COMPLAINT ----------------------
@api.route('/complaint')
def complaint():
    data = {}
    title = request.args['title']
    Description = request.args['Description']
    care_id = request.args['cid']

    qry = "insert into complaints values(null,'%s','%s','%s','pending',curdate())" % (care_id, title, Description)
    insert(qry)

    data['status'] = 'success'
    return jsonify(data)


# ------------------- MANAGE PATIENT ----------------------
@api.route('/managepatients')
def managepatients():
    data = {}
    fname = request.args['fname']
    lname = request.args['lname']
    gender = request.args['gender']
    Dob = request.args['dob']
    caretakerid = request.args['caretakerid']
    username = request.args['username']
    password = request.args['password']

    print(username, password)

    a = "insert into login values(null,'%s','%s','patient')" % (username, password)
    b = insert(a)

    c = "insert into patient values(null,'%s','%s','%s','%s','%s','%s')" % (b, caretakerid, fname, lname, gender, Dob)
    res = insert(c)

    if res:
        data['status'] = 'success'
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- VIEW REMINDER ----------------------
@api.route('/viewreminder')
def viewreminder():
    data = {}
    lid = request.args['lid']

    qry = "select * from remainder where patient_id=(select patient_id from patient where login_id='%s')" % (lid)
    res = select(qry)

    if res:
        data['status'] = 'success'
        data['data'] = res
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- VIEW DOCTORS ----------------------
@api.route('/viewdoctors')
def viewdoctors():
    data = {}

    qry = "select * from doctors"
    res = select(qry)

    if res:
        data['status'] = 'success'
        data['data'] = res
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- VIEW PATIENTS ----------------------
@api.route('/patientslists')
def patientslists():
    data = {}

    qry = "select * from patient"
    res = select(qry)

    if res:
        data['status'] = 'success'
        data['data'] = res
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- VIEW REPLY ----------------------
@api.route('/viewreply')
def viewreply():
    data = {}
    lid = request.args['lid']

    qry = "select * from complaints where caretaker_id='%s'" % (lid)
    res = select(qry)

    if res:
        data['status'] = 'success'
        data['data'] = res
    else:
        data['status'] = 'failed'

    return jsonify(data)


# ------------------- ADD VISITORS ----------------------
@api.route('/add_visitors', methods=['POST'])
def add_visitors():
    data = {}

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    category = request.form['category']
    address = request.form['address']
    dob = request.form['dob']
    gender = request.form['gender']

    image1 = request.files['image']
    image2 = request.files['image1']
    image3 = request.files['image2']

    qry = "insert into visitors values(null,'%s','%s','%s','%s','%s','%s','pending')" % (
        category, first_name, last_name, address, gender, dob)
    pid = insert(qry)

    folder = "static/trainimages/" + str(pid)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    path1 = folder + "/imag1.jpg"
    path2 = folder + "/imag2.jpg"
    path3 = folder + "/imag3.jpg"

    image1.save(path1)
    image2.save(path2)
    image3.save(path3)

    qry1 = "update visitors set image='%s' where visitors_id='%s'" % (path1, pid)
    update(qry1)

    enf(r"static/trainimages/")

    data['status'] = "success"
    return jsonify(data)
