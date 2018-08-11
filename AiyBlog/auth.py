import time

from flask import Blueprint,request,session,render_template,redirect,url_for

from AiyBlog import db
from AiyBlog.models import aiyblog_users
from AiyBlog.utils import pwd2hash,authed

auth = Blueprint("auth",__name__,url_prefix='/auth')

@auth.route('/login',methods=["GET","POST"])
def login():

    if authed():
        return redirect(url_for("views.index"))
    if request.method == "POST":
        errors = []
        name = request.form["username"]
        user = aiyblog_users.query.filter_by(name=name).first()


        if user and (request.form["password"])==user.password:
            print('0000')
            session["username"] = user.name
            session["uid"] = user.uid
            session["admin"] = user.group
            user.activated = int(time.time())
            # user.activated = 123
            # print(user.activated)
            db.session.commit()
            db.session.close()

            # login successful
            return redirect(url_for("admin.admin_index"))
        #the user is exists but the password is wrong
        else:

            errors.append("你的用户名或者密码不正确!")
            db.session.close()
            print("11111")
            return render_template("admin/auth/login.html",errors=errors)

    return render_template("admin/auth/login.html")

@auth.route('/register',methods=["GET","POST"])
def register():

    if request.method == "POST":
        errors = []
        username = request.form["username"]
        password = request.form["password"]

        if aiyblog_users.query.filter_by(name=username).first():
            errors.append("用户名已存在!")


        if len(errors)==0:
            u = aiyblog_users(name=username,password=pwd2hash(password.encode("utf-8")),created=int(time.time()))
            db.session.add(u)
            db.session.commit()
            db.session.close()
        else:
            return render_template("admin/auth/register.html",errors=errors)



    return render_template("admin/auth/register.html")


@auth.route('/logout')
def logout():
    if authed():
        session.clear()
        return redirect(url_for("auth.login"))
    else:
        return redirect(url_for("auth.login"))


