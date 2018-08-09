from flask import Blueprint

from flask import render_template
from AiyBlog.utils import admins_only
from AiyBlog.models import aiyblog_contents,aiyblog_users,aiyblog_metas,aiyblog_comments

admin = Blueprint("admin",__name__,url_prefix="/admin")

@admin.route('/',methods=["GET"])
# @admins_only
def admin_index():

    contents = aiyblog_contents.query.count()

    comments = aiyblog_comments.query.count()

    categories = aiyblog_metas.query.filter_by(type="category").count()

    index = [contents,comments,categories]

    return render_template("admin/console/index.html",index=index)

