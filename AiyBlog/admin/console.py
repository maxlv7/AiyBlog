import time
from flask import Blueprint
from flask import render_template,request,redirect,url_for,session

from AiyBlog import db
from AiyBlog.models import aiyblog_users,aiyblog_contents,aiyblog_comments,aiyblog_metas
console = Blueprint(__name__,"console",url_prefix='/admin/console')


@console.route('/profile',methods=["GET","POST"])
def profile():

    user = aiyblog_users.query.filter_by(uid=session["uid"]).first()

    content_nums = aiyblog_contents.query.filter_by(authorId=session["uid"]).count()
    comment_nums = aiyblog_comments.query.filter_by(authorId=session["uid"]).count()
    category_nums = aiyblog_metas.query.filter_by(type="category").count()
    activated = time.localtime(user.activated)

    if request.method == "POST":

        try:
            nickname = request.form["nickname"]
            url = request.form["url"]
            email = request.form["email"]
        except:
            pass
        else:
            user = aiyblog_users.query.filter_by(uid=session["uid"]).first()
            user.screenName = nickname
            user.url = url
            user.mail = email
            db.session.commit()
        return redirect(url_for("AiyBlog.admin.console.profile"))

    return render_template("admin/console/profile.html",user=user,ctn = content_nums,cmn=comment_nums,cgm=category_nums,activated=activated)