import os

from flask import Blueprint,send_file,safe_join,abort,render_template,session
from flask import current_app as app
from AiyBlog.models import aiyblog_users,aiyblog_options,aiyblog_contents,aiyblog_metas

from sqlalchemy import desc
views = Blueprint("views",__name__)

'''
This is user interface

'''

@views.route('/index')
@views.route('/')
def index():
    """
        index:
        一定数量的文章 10。
        所有独立页面。

    """
    blogs = aiyblog_contents.query.filter_by(type="post").order_by(desc(aiyblog_contents.created)).all()
    pages = aiyblog_contents.query.filter_by(type="page").order_by(aiyblog_contents.order).all()

    new_articles = aiyblog_contents.query.filter_by(type="post").order_by(desc(aiyblog_contents.created)).limit(10).all()

    categories = aiyblog_metas.query.filter_by(type="category").all()

    return render_template('index.html',blogs=blogs,pages=pages,new_articles=new_articles,\
                           categories=categories)



@views.route('/archives/<int:cid>')
def archives(cid):

    blog = aiyblog_contents.query.filter_by(cid=cid).first()
    if blog is None:
        abort(404)
    pages = aiyblog_contents.query.filter_by(type="page").order_by(aiyblog_contents.order).all()
    new_articles = aiyblog_contents.query.filter_by(type="post").order_by(desc(aiyblog_contents.created)).limit(10).all()
    categories = aiyblog_metas.query.filter_by(type="category").all()

    return render_template("post.html",blog=blog,pages=pages,new_articles=new_articles,\
                           categories=categories)

@views.route('/themes/<theme>/static/<path:path>')
def themes_handler(theme, path):
    filename = safe_join(app.root_path, 'themes', theme, 'static', path)
    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)


@views.route('/index/<path:path>')
def pages_handler(path):
    pages = aiyblog_contents.query.filter_by(type="page").order_by(aiyblog_contents.order).all()
    new_articles = aiyblog_contents.query.filter_by(type="post").order_by(desc(aiyblog_contents.created)).limit(10).all()
    categories = aiyblog_metas.query.filter_by(type="category").all()

    if type(path) == int:
        blog = aiyblog_contents.query.filter_by(cid=path).first()
    else:
        blog = aiyblog_contents.query.filter_by(slug=path).first()

    return render_template("page.html",blog=blog,\
                           pages=pages,categories=categories,new_articles=new_articles)