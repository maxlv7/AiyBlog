import time

from flask import Blueprint
from flask import render_template,request,url_for,redirect,session
from AiyBlog import db
from AiyBlog.models import aiyblog_metas,aiyblog_contents,aiyblog_relationships
from AiyBlog.utils import find_mid_by_cid
write = Blueprint(__name__,"write",url_prefix="/admin/write")

@write.route('/post',methods=["GET","POST"])
def post():

    categories = aiyblog_metas.query.filter_by(type="category").all()
    tags = aiyblog_metas.query.filter_by(type="tag").all()

    #修改文章
    if request.args.get("cid"):
        cid = request.args.get("cid")
        blog = aiyblog_contents.query.filter_by(cid=cid).first()
        return render_template("admin/write/post.html", cat=categories,blog=blog)

    return render_template("admin/write/post.html",cat=categories)

@write.route('/page',methods=["GET","POST"])
def page():

    if request.method == "POST":
        title = request.form["title"] or "未命名页面"
        slug = request.form["slug"]
        text = request.form["markdown"]
        order = int(request.form["order"])
        status = request.form["visibility"]
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        page = aiyblog_contents(title=title,slug=slug,text=text,type="page",created=time.time(),status=status,\
                                allowComment=allowComments,order=order,authorId=session["uid"]
                                )
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("AiyBlog.admin.manage.posts"))

    return render_template("admin/write/page.html")
