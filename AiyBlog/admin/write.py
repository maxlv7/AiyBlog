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
        return render_template("admin/write/post.html", cat=categories,tags=tags,blog=blog)

    return render_template("admin/write/post.html",cat=categories,tags=tags)

@write.route('/page',methods=["GET","POST"])
def page():
    if request.args.get("cid"):
        cid = request.args.get("cid")
        page = aiyblog_contents.query.filter_by(cid=cid).first()
        return render_template("admin/write/page.html",page=page)
    return render_template("admin/write/page.html")
