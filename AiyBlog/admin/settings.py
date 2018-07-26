from flask import Blueprint
from flask import render_template,request,url_for,redirect
from AiyBlog.utils import set_config
settings = Blueprint(__name__,"settings",url_prefix='/admin/options')

@settings.route('/base',methods=["GET","POST"])
def base():

    if request.method == "POST":

        siteName = request.form["siteName"]
        siteUrl = request.form["siteUrl"]
        siteDescription = request.form["siteDescription"]
        siteKeyword = request.form["siteKeyword"]
        allowRegister = request.form["allowRegister"]

        set_config("siteName",siteName)
        set_config("siteUrl",siteUrl)
        set_config("siteDescription",siteDescription)
        set_config("siteKeyword",siteKeyword)
        set_config("allowRegister",allowRegister)
        return redirect(url_for("AiyBlog.admin.settings.base"))

    return render_template("admin/settings/base.html")