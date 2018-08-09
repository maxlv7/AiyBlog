from flask import Blueprint
from flask import render_template,request,redirect,url_for

from AiyBlog.models import aiyblog_contents,aiyblog_relationships,aiyblog_metas
from sqlalchemy import desc

manage = Blueprint(__name__,"manage",url_prefix='/admin/manage')

@manage.route('/posts',methods=["GET","POST"])
def posts():

    blogs = aiyblog_contents.query.filter_by(type="post").order_by(desc(aiyblog_contents.created)).all()

    return render_template("admin/manage/manage-posts.html",blogs=blogs)

@manage.route('/categories',methods=["GET","POST"])
def categories():
    if request.args.get("mid"):
        mid = request.args.get("mid")
        category = aiyblog_metas.query.filter_by(mid=mid).first()
        return render_template("admin/manage/category.html",category=category)

    cgs = aiyblog_metas.query.filter_by(type="category").all()

    return render_template("admin/manage/manage-categories.html",cgs=cgs)

@manage.route('/create/category')
def create_cg():

    return render_template("admin/manage/category.html")

@manage.route('/pages')
def pages():
    pages = aiyblog_contents.query.filter_by(type="page").all()

    return render_template("admin/manage/manage-pages.html", pages=pages)

@manage.route('/tags')
def tags():

    if request.args.get("mid"):
        mid = request.args.get("mid")
        tag = aiyblog_metas.query.filter_by(mid=mid).first()
        tags = aiyblog_metas.query.filter_by(type="tag").all()
        return render_template("admin/manage/manage-tags.html", tag=tag,tags=tags)

    tags = aiyblog_metas.query.filter_by(type="tag").order_by(aiyblog_metas.mid).all()

    return render_template("admin/manage/manage-tags.html",tags=tags)

