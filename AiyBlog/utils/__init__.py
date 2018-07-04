import functools

from flask import current_app as app
from flask import render_template,session,abort
from werkzeug.security import generate_password_hash,check_password_hash

from AiyBlog.models import aiyblog_users
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


def authed():
    #when the uid is not esist,the default value is False
    return bool(session.get("uid",False))

def is_admin():
    if authed():
        return session["admin"]
    else:
        return False


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
    return generate_password_hash(password)

def check_hash(hash,password):
    return check_password_hash(hash,password)


if __name__ == '__main__':

    print(checkpwd())
