import time

from flask import Blueprint
from flask import render_template,request,url_for,redirect,session
from AiyBlog import db
from AiyBlog.models import aiyblog_metas,aiyblog_contents,aiyblog_relationships

write = Blueprint(__name__,"write",url_prefix="/admin/write")

@write.route('/post',methods=["GET","POST"])
def post():

    categories = aiyblog_metas.query.filter_by(type="category").all()
    tags = aiyblog_metas.query.filter_by(type="tag").all()

    #写文章
    if request.method == "POST":

        cgs = request.form.getlist("category[]")
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]
        status = request.form["visibility"]
        raw_tags = request.form["tags"]

        new_tags = raw_tags.replace('，',',').split(',')

        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        # some oper
        content = aiyblog_contents(title=title,created=int(time.time()),text=text,type="post",\
                                   status=status,allowComment=allowComments,authorId=session["uid"])
        db.session.add(content)
        db.session.commit()

        # 先拿到cid,然后再找到对应的mid关系
        cid = content.cid
        #用户没有选择分类，那么为默认分类
        if len(cgs)==0:
            relationship = aiyblog_relationships(cid=cid, mid=2)
            db.session.add(relationship)
            db.session.commit()
        else:
            for mid in cgs:
                relationship = aiyblog_relationships(cid=cid,mid=mid)
                db.session.add(relationship)
                db.session.commit()

        return redirect(url_for("AiyBlog.admin.write.post"))


    #修改文章
    if request.args.get("cid"):
        cid = request.args.get("cid")
        blog = aiyblog_contents.query.filter_by(cid=cid).first()
        return render_template("admin/write/post.html", cat=categories,blog=blog)
    else:
        print(2)

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
        return redirect(url_for("AiyBlog.admin.write.page"))

    return render_template("admin/write/page.html")
