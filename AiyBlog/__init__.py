import os

from config import config

from flask import Flask
from jinja2 import FileSystemLoader
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ThemeLoader(FileSystemLoader):
    """Custom FileSystemLoader that switches themes based on the configuration value"""
    def __init__(self, searchpath, encoding='utf-8', followlinks=False):
        super(ThemeLoader, self).__init__(searchpath, encoding, followlinks)
        self.overriden_templates = {}

    def get_source(self, environment, template):
        # Check if the template has been overriden
        if template in self.overriden_templates:
            return self.overriden_templates[template], template, True

        # Check if the template requested is for the admin panel
        if template.startswith('admin/'):
            template = template[6:]  # Strip out admin/
            template = "/".join(['admin', 'templates', template])
            return super(ThemeLoader, self).get_source(environment, template)

        # Load regular theme data
        # theme = utils.get_config('aiyblog_theme')
        template = "/".join(["default", 'templates', template])
        return super(ThemeLoader, self).get_source(environment, template)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])


    # reset jinja2 default templates folder
    # this folder is app.root_path/themes
    theme_loader = ThemeLoader(os.path.join(app.root_path, 'themes'), followlinks=True)
    app.jinja_loader = theme_loader

    # init expand
    db.init_app(app)

    # init utils
    from AiyBlog import utils

    utils.init_errors(app)
    utils.init_utils(app)


    # register blueprint
    from AiyBlog.auth import auth
    from AiyBlog.admin import admin
    from AiyBlog.admin.settings import settings
    from AiyBlog.admin.write import write
    from AiyBlog.admin.console import console
    from AiyBlog.views import views

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(views)
    app.register_blueprint(settings)
    app.register_blueprint(write)
    app.register_blueprint(console)

    return app

