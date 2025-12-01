import os
from flask import *
from face_model import *
from facedetection import *


from database import *


api=Blueprint('api',__name__)


@api.route('/reg')
def reg():
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    email=request.args['email']
    phone=request.args['phone']
    place=request.args['place']
    gender=request.args['gender']
    username=request.args['username']
    password=request.args['password']
    print(fname,lname,email,phone,place,gender,username,password)

    a="insert into login values(null,'%s','%s','caretaker')"%(username,password)
    b=insert(a)
       
    c="insert into caretaker values(null,'%s','%s','%s','%s','%s','%s','%s')"%(b,fname,lname,email,phone,gender,place,)
    res=insert(c)
    if res:
        data['status']='sucess'
    else:
        data['status']='failed'    
    return str(data)

@api.route('/log')
def log():
    data={}
    username=request.args['username']
    password=request.args['password']
    print(username,password)
    a= "select * from login INNER JOIN caretaker ON login.loginid = caretaker.login_id where username='%s'and password='%s'"%(username,password)
    res=select(a)
    if res:
      
        data['status']='success'
        data['view']=res
 
    else:
        b="select * from login where username='%s' and password='%s'"%(username,password)
        x=select(b)
        if x:
            data['status']="patient"
            data['view']=x
        


 
  

    print(data)
    return str(data)


@api.route('/complaint')
def complaint():
    data={}
    title=request.args['title']
    Description=request.args['Description']
    care_id=request.args['cid']
    print(title,Description)


    # a="select * from login where username='%s'and password='%s'"%(username,password)
    # res=select(a)
    a="insert into complaints values(null,'%s','%s','%s','pending',curdate())"%(care_id,title,Description)
    b=insert(a)


    

    return str(data)


@api.route('/managepatients')
def managepatients():
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    gender=request.args['gender']
    Dob=request.args['dob']
    caretakerid=request.args['caretakerid']
    username=request.args['username']
    password=request.args['password']
    print(username,password)

    a="insert into login values(null,'%s','%s','patient')"%(username,password)
    b=insert(a)
       
    c="insert into patient values(null,'%s','%s','%s','%s','%s','%s')"%(b,caretakerid,fname,lname,gender,Dob)
    res=insert(c)
    if res:
        data['status']='sucess'
    else:
        data['status']='failed'    
    return str(data)


@api.route('/viewreminder')
def viewreminder():
    data={}
    lid=request.args['lid']
    print(lid,"/////////")
    a="select * from remainder where patient_id=(select patient_id from patient where login_id='%s')"%(lid)
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewreminder'  
    return str(data)




@api.route('/viewvisitors')
def viewvisitors():
    data={}
    category_id=request.args["category_id"]
    print(category_id,"/////////")
    a="select * from visitors where category_id=(select category_id from visitorscategory where category_id='%s')"%(category_id)
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewvisitors'  
    return str(data)



@api.route('/viewprescription')
def viewprescription():
    data={}
    appointment_id=request.args['appointment_id']
    a="select * from prescription where appointment_id='%s'"%(appointment_id)
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewprescription'  
    return str(data)

@api.route('/view_appointment')
def view_appointment():
    data={}
    c_id=request.args['c_id']
    a="SELECT * FROM appointment INNER JOIN patient USING(patient_id) INNER JOIN caretaker USING(caretaker_id) INNER JOIN doctors USING(doctor_id) WHERE caretaker.login_id='%s' ORDER BY appointment.patient_id"%(c_id)
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewappointment'  

    print(data,"((((((((()))))))))")
    return str(data)

@api.route('/viewdoctors')
def viewdoctors():
    data={}
    lid=request.args['lid']
    print(lid,"/////////")
    a="select * from doctors"
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewdoctors'  
    return str(data)





@api.route('/patientslists')
def patientslists():
    data={}
    lid=request.args['lid']
    print(lid,"/////////")
    a="select * from patient"
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='patientslist'  
    print(data,"&&&&&&&&&&&&&&&&")
    return str(data)



@api.route('/add_visitor_category')
def add_visitor_category():
    data={}
    description=request.args['description']
    patient_id=request.args['patient_id']

    qry="insert into visitorscategory values(null,'%s','%s')"%(patient_id,description)
    res=insert(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="added"
    return str(data)


@api.route('/view_visitor_category')
def  view_visitor_category():
    data={}
   
     
    qry="select * from visitorscategory"
    res=select(qry)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='view'

    
    return str(data)


@api.route('/add_remainder_category')
def  add_remainder_category():
    data={}
    category_name=request.args['addremainder']
    patid=request.args['patid']
    

    qry="insert into remainder_category values(null,'%s','%s')"%(category_name,patid)
    res=insert(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="added"
    return str(data)



@api.route('/view_remainder_category')
def  view_remainder_category():
    data={}
   
     
    qry="select * from remainder_category"
    res=select(qry)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='view'

    
    return str(data)



@api.route('/makeappointment')
def  makeappointment():
    data={}
    date=request.args['date']
    doctor_id=request.args['docid']
    patient_id=request.args['pid']

    print(doctor_id,date,patient_id,"//////////////////////////23456789///////**********")

    qry="insert into appointment values(null,'%s','%s','%s','pending')"%(doctor_id,patient_id,date)
    res=insert(qry)
    
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']='makeappointment'
    return str(data)



@api.route('/patientappointment')
def patientappointment():
    data={}
    lid=request.args['lid']
    print(lid,"/////////")
    a="select * from patient"
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='patientappointment'  
    return str(data)


@api.route('/viewreply')
def viewreply():
    data={}
    lid=request.args['lid']
    print(lid,"/////////")
    a="select * from complaints where caretaker_id='%s'"%(lid)
    res=select(a)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'  
    data['method']='viewreply'  
    return str(data)


@api.route('/feedback')
def feedback():
    data={}
    Description=request.args['Description']
    care_id=request.args['cid']
    print(care_id,Description)


    # a="select * from login where username='%s'and password='%s'"%(username,password)
    # res=select(a)
    a="insert into feedback values(null,'%s','%s',curdate())"%(care_id,Description)
    b=insert(a)


    

    return str(data)




@api.route('/manage_remainder')
def manage_remainder():
    data={}
    rem_title=request.args['rem_title']
    rem_desc=request.args['rem_desc']
    rem_time=request.args['rem_time']
    rem_date=request.args['rem_date']
    catid=request.args['catid']
    print(rem_title,rem_desc,rem_time,rem_date,catid)
    time="0"+rem_time

    qry="insert into remainder values(null,'%s','%s','%s','%s','%s')"%(catid,rem_title,rem_desc,time,rem_date)
    res=insert(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']='manage_remainder'


    return str(data)



@api.route('/view_remainderss')
def view_remainderss():
    data={}
    id=request.args['id']
    current_date = datetime.now().strftime('%Y-%m-%d')

    print(current_date)
    current_time = datetime.now().strftime("%I:%M %p").lower()

    print(current_time)
    qry="select * from remainder inner join remainder_category using(remainder_category_id) where patient_id=(select patient_id from patient where login_id='%s') and date='%s' and time='%s'"%(id,current_date,current_time)
    res=select(qry)
    print(res,"'")
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="rem"
    return str(data)






    


    











    





    




    





    





    




    




@api.route('/add_visitors',methods=['get','post'])
def add_visitors():
    data={}
    print("00000000000000000000000000000000000000000")
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    category=request.form['category']
    address=request.form['address']
    dob=request.form['dob']
    gender=request.form['gender']
    image1=request.files['image']

   
    
 
    
    qry="insert into visitors values(null,'%s','%s','%s','%s','%s','%s','pending')"%(category,first_name,last_name,address,gender,dob)
    id1=insert(qry)
    
    pid = str(id1)
    
    isFile = os.path.isdir(r"static/trainimages/" + pid)  
    print(isFile)
    if not isFile:
        os.mkdir(r'static/trainimages/' + pid)
        path1 = "static/trainimages/" + pid + "/imag1.jpg"
        image1.save(path1)
        print(path1,"--------------------------------")
        
        image2 = request.files['image1']
        path2 = "static/trainimages/" + pid + "/imag2.jpg"
        image2.save(path2)
        
        image3 = request.files['image2']
        path3 = "static/trainimages/" + pid + "/imag3.jpg"
        image3.save(path3)
        
        qry1="update visitors set image='%s' where visitors_id='%s'"%(path1,pid)
        r=update(qry1)
        
        enf(r"static/trainimages/")
        if r:
            data['status']="success"
        else:
            data['status']="failed"






    return str(data)
    



@api.route('/face_check/',methods=['get','post'])
def face_check():
    data={}
    image=request.files['image']
    idss=request.form['id']
    image.save("static/assets/img/" + "test.jpg")
    path="static/assets/img/" + "test.jpg"
    qh=rec_face_image(path)
    print(qh,idss,"---"*1000)
    if qh:
        print("Haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        q="select  * from visitors inner join visitorscategory using(category_id) where visitors_id='%s' and patient_id=(select patient_id from patient where login_id='%s')" %(qh[0],idss)
        res=select(q)
        if res:
            print(res)
            data['status']="success"
            data['data']= "Person is Identified and the name is : "+ res[0]['first_name']+res[0]['last_name'] +"Address is :"+res[0]['address'] +"and the category is :"+res[0]['category_name']
        else:
            data['data']="unknown person not yet in your visitor list...!"
    else:
        data['data']="unknown person"

    data['status']="success"
    data['action']="face_check"

    return  str(data)




@api.route('/accessphone')
def accessphone():
    data={}
    id=request.args['id']

    qry="select * from caretaker inner join patient where patient.login_id='%s'"%(id)
    res=select(qry)
    print(res,"---------")
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="phone"
    return str(data)