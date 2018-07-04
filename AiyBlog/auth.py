from flask import Blueprint,request,session,render_template

from AiyBlog import db
from AiyBlog.models import aiyblog_users
from AiyBlog.utils import check_hash,authed
auth = Blueprint("auth",__name__,url_prefix='/auth')

@auth.route('/login',methods=["GET","POST"])
def login():

    if request.method == "POST":
        errors = []
        name = request.form["name"]
        user = aiyblog_users.query.filter_by(name=name).first()
        if user:
            if user and check_hash(user.password,request.form["password"]):

                session["username"] = user.name
                session["uid"] = user.uid
                session["admin"] = user.group
                db.session.close()

            #the user is exists but the password is wrong
            else:

                errors.append("Your username or password is incorrect!")
                db.session.close()

                return render_template("admin/login.html",errors=errors)

    return render_template("admin/login.html")


@auth.route('/logout')
def logout():
    if authed():
        session.clear()
    return "xxx"


