from flask import *

from database import *
import uuid

Doctor=Blueprint('Doctor',__name__)


@Doctor.route ("/Doctorhome")
def Doctorhome():
    return render_template("Doctorhome.html")

@Doctor.route ("/viewappointment")
def viewappointment():
    data={}
    qry="select * from appointment inner join patient using(patient_id)"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("viewappointment.html",data=data)



@Doctor.route ("/viewpatient")
def viewpatient():
    id=request.args['id']
    data={}
    qry="SELECT * FROM patient INNER JOIN appointment USING(patient_id)"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("viewpatient.html",data=data)




@Doctor.route ("/addprescription" ,methods=['POST','GET'])
def addprescription():
    aid=request.args['id']
    

   
    if 'submit' in request.form:
        addprescription=request.form['addprescription']

        c="insert into prescription values(null,'%s','%s',curdate())"%(aid,addprescription)
        insert(c)
        return "<script>alert('Added');window.location='/viewappointment'</script>"
    return render_template('addprescription.html')

@Doctor.route ("/add_additional_documents" ,methods=['POST','GET'])
def add_additional_documents():
    aid=request.args['id']
    if 'submit' in request.form:
        add_additional_documents=request.files['additionaldocuments']
        path="static/"+str(uuid.uuid4())+add_additional_documents.filename
        add_additional_documents.save(path)
        c="insert into additionaldocuments values(null,'%s','%s',curdate())"%(aid,path)
        d=insert(c)
        print
        if d:
            return "<script>alert('Added');window.location='/viewappointment'</script>"
    return render_template('additionaldocuments.html')


@Doctor.route ("/doctorviewfeeback")
def doctorviewfeeback():
    data={}
    qry="select * from feedback"
    res=select(qry)
    if res:
        data['view']=res
    return render_template('doctorviewfeeback.html',data=data)
 










