import functools
import hashlib
from flask import current_app as app
from flask import render_template,session,abort

from AiyBlog import db
from AiyBlog.models import aiyblog_users,aiyblog_options

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
    app.jinja_env.globals.update(get_config=get_config)
    app.jinja_env.globals.update(set_config=set_config)


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

    print(generate_password_hash("123"))
    print(check_password_hash("pbkdf2:sha256:50000$714BNkeq$b548df6ffa698fc14f9bf6c3793cc05b3c1","123"))
