from flask import *

from database import *

admin=Blueprint('admin',__name__)

@admin.route ("/adminhome")
def adminhome():
    return render_template("adminhome.html")


@admin.route ("/viewcaretakers")
def viewcaretakers():
    data={}
    qry="select * from caretaker"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("viewcaretakers.html",data=data)


@admin.route ("/viewcomplaints")
def viewcomplaints():
    data={}
    qry="select * from complaints"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("viewcomplaints.html",data=data)






@admin.route ("/reply" ,methods=['POST','GET'])
def reply():
    id=request.args['id']
    if 'submit' in request.form:
        reply=request.form['reply']

        qry="update complaints set reply='%s'  where complaint_id='%s'"%(reply,id)
        update(qry)
    return render_template("reply.html")

@admin.route ("/admin_viewpatient")
def admin_viewpatient():
    data={}
    qry="select * from patient"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("admin_viewpatient.html",data=data)


@admin.route ("/adminviewfeeback")
def adminviewfeeback():
    data={}
    qry="select * from feedback"
    res=select(qry)
    if res:
        data['view']=res
    return render_template('adminviewfeeback.html',data=data)
    
    
@admin.route ("/viewreview")
def viewreview():
    data={}
    qry="select * from review"
    res=select(qry)
    if res:
        data['view']=res
    return render_template('viewreview.html',data=data)


    
    














