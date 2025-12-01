from flask import*
from database import*

public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template("home.html")    

@public.route('/login',methods=['get','post'])
def login():
    if 'submit' in request.form:
     username=request.form["username"]
     password=request.form["password"]
     print(username,password)
     a="select * from login where username='%s'and password='%s'"%(username,password)
     res=select(a)
     if res :
        session['lid']=res[0]['loginid']
        print(session['lid'],"////")
        if res[0]['usertype']==('Doctor'):
           return redirect(url_for('Doctor.Doctorhome'))
        if res[0]['usertype']=='admin':
           return redirect(url_for('admin.adminhome'))
        if res[0]['usertype']==('caretaker'):
           return redirect(url_for('caretaker.caretakerhome'))
        
        elif res[0]['usertype']=='user':
           z="select * from doctor where loginid='%s'"%(session['lid'])
           x=select(z)
           session['rid']=x[0]['reg_id']
           print(session['rid'],"////////////rid")
           return redirect(url_for('user.userhome'))
    return render_template("login.html")
     
# @public.route('/doctor',methods=['get','post'])
# def doctor():
#     return render_template("doctor.html")

@public.route('/doctors', methods=['get','post'])
def doctors():
    if 'submit' in request.form:
       fname=request.form["fname"]
       lname=request.form["lname"]
       place=request.form["place"]
       email=request.form["email"]
       phone=request.form["phone"]
       username=request.form["username"]
       password=request.form["password"]
       qualification=request.form["qualification"]
       print(fname,lname,place,email,phone,username,password,qualification)

       a="insert into login values(null,'%s','%s','Doctor')"%(username,password)
       b=insert(a)
       
       c="insert into doctors values(null,'%s','%s','%s','%s','%s','%s','%s')"%(b,fname,lname,place,phone,email,qualification)
       insert(c)


    return render_template("doctor.html")

     

@public.route('/caretaker', methods=['get','post'])
def caretaker():
    if 'submit' in request.form:
       fname=request.form["fname"]
       lname=request.form["lname"]
       email=request.form["email"]
       phone=request.form["phone"]
       gender=request.form["gender"]
       place=request.form["place"]
       username=request.form["username"]
       password=request.form["password"]
       print(fname,lname,email,phone,gender,place,username,password,)

       a="insert into login values(null,'%s','%s','caretaker')"%(username,password)
       b=insert(a)
       
       c="insert into caretaker values(null,'%s','%s','%s','%s','%s','%s','%s')"%(b,fname,lname,email,phone,gender,place)
       insert(c)


    return render_template("caretaker.html")


