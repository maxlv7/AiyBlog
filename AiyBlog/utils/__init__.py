import functools,hashlib,time

from flask import current_app as app
from flask import render_template,session,abort,request

from AiyBlog import db
from AiyBlog.models import aiyblog_users,aiyblog_options,aiyblog_relationships,aiyblog_metas

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return error.description,404

    @app.errorhandler(403)
    def forbidden(error):
        return error.description,403

    @app.errorhandler(500)
    def general_error(error):
        return error.description,500

    @app.errorhandler(502)
    def gateway_error(error):
        return error.description,502


def init_utils(app):

    #jinja2全局变量
    app.jinja_env.globals.update(get_config=get_config)
    app.jinja_env.globals.update(set_config=set_config)
    app.jinja_env.globals.update(get_name_by_id=authorId2name)
    app.jinja_env.globals.update(find_mid_by_cid=find_mid_by_cid)
    app.jinja_env.globals.update(get_cgs_by_cid=get_cgs_by_cid)
    app.jinja_env.globals.update(get_tags_by_cid=get_tags_by_cid)

    #jinja2 拓展，实现break和continue
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    #jinja2 自定义过滤器
    app.jinja_env.filters["showtime"] = showtime
    app.jinja_env.filters["showcategories"] = showcategories


    @app.before_request
    def check_admin():
        path = request.path
        if path.startswith('/admin'):
            if not is_admin():
                abort(403)


def showcategories(l:list):
    des = []
    for c in l:
        u = aiyblog_metas.query.filter_by(mid=c).first()
        des.append(u.name)
    if len(des) == 1:
        return des
    else:
        cp = []
        for x in des:
            cp.append(x)
            cp.append(",")

        cp.pop()
        return cp

#通过cid找到分类
def get_cgs_by_cid(cid):
    categories = list()
    cgs_list = find_mid_by_cid(int(cid))

    for c in cgs_list:
        cg = aiyblog_metas.query.filter_by(mid=c,type='category').first()
        if cg!=None:
            categories.append(cg.name)
    return categories

#通过cid找到标签
def get_tags_by_cid(cid):
    tags = list()

    tags_list = find_mid_by_cid(int(cid))
    for c in tags_list:
        cg = aiyblog_metas.query.filter_by(mid=c,type='tag').first()
        if cg!=None:
            tags.append(cg.mid)
    return tags

#jinja2 自定义过滤器,根据unix时间戳返回显示时间
def showtime(oldtime):
    nowtime = int(time.time())
    times = nowtime - oldtime
    if times >= 0 and times < 60:
        return str(times+1)+"秒前"
    if times >= 60 and times < 3600:
        return str(times//60)+"分前"
    if times >= 3600 and times < 86400:
        return str(times//3600) + "小时前"
    if times >= 86400:
        return str(time.localtime(oldtime)[0])+"年" + str(time.localtime(oldtime)[1])+"月"+str(time.localtime(oldtime)[2])+"日"

#通过cid找到mid的对应关系
def find_mid_by_cid(cid):

    realtionship = list()
    res = aiyblog_relationships.query.filter_by(cid=cid).all()
    for r in res:
        realtionship.append(r.mid)
    return realtionship


def authorId2name(id):
    user = aiyblog_users.query.filter_by(uid=id).first()
    # print(user.name+"............")
    return user.screenName or user.name

def authed():
    #when the uid is not esist,the default value is False
    return bool(session.get("uid",False))

def is_admin():
    if authed():
        return session["admin"]
    else:
        return False


def set_config(key,value):
    config = aiyblog_options.query.filter_by(name=key).first()
    if config:
        config.value = value
    else:
        config = aiyblog_options(name=key,value=value)
        db.session.add(config)
    db.session.commit()
    return None


def get_config(key):
    config = aiyblog_options.query.filter_by(name=key).first()
    if config:
        return config.value
    else:
        return none

def authed_only(f):
    """
    Decorator that requires the user to be authenticated
    :param f:
    :return:
    """
    @functools.wraps(f)
    def defcorate_func(*args,**kwargs):
        if session.get("uid"):
            return f(*args,**kwargs)
        else:
            return abort(403)
    return defcorate_func

def admins_only(f):
    """
    Decorator that requires the user to be authenticated and an admin
    :param f:
    :return:
    """
    @functools.wraps(f)
    def decorate_func(*args,**kwargs):
        if session.get("admin"):
            return f(*kwargs,**kwargs)
        else:
            return abort(403)
    return decorate_func

def pwd2hash(password):
    return hashlib.sha1(password).hexdigest()



if __name__ == '__main__':

    pass