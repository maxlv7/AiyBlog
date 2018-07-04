from flask import Blueprint

from AiyBlog.utils import admins_only
admin = Blueprint("admin",__name__)

@admin.route('/admin',methods=["GET"])
@admins_only
def admin_index():
    return "ok"