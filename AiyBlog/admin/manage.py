from flask import Blueprint
from flask import render_template,request,redirect,url_for

from AiyBlog.models import aiyblog_contents,aiyblog_relationships
from AiyBlog import db

manage = Blueprint(__name__,"manage",url_prefix='/admin/manage')

@manage.route('/posts',methods=["GET","POST"])
def posts():

    blogs = aiyblog_contents.query.filter_by(type="post").all()

    return render_template("admin/manage/posts.html",blogs=blogs)