from AiyBlog import db

class aiyblog_comments(db.Model):

    __tablename__ = 'aiyblog_comments'

    coid = db.Column(db.Integer,primary_key=True,nullable=False,default="NULL",autoincrement=True)
    cid = db.Column(db.Integer,default=0)
    created = db.Column(db.Integer,default=0)
    author = db.Column(db.String(200),default="NULL")
    authorId = db.Column(db.Integer,default=0)
    owenerId = db.Column(db.Integer,default=0)
    mail = db.Column(db.String(200),default="NULL")
    url = db.Column(db.String(200),default="NULL")
    ip = db.Column(db.String(64),default="NULL")
    agent = db.Column(db.String(200),default="NULL")
    text = db.Column(db.Text,default="NULL")
    type = db.Column(db.String(16),default="comment")
    status = db.Column(db.String(16),default="approved")
    parent = db.Column(db.Integer,default=0)

class aiyblog_contents(db.Model):

    __tablename__ = 'aiyblog_contents'

    cid = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    title = db.Column(db.String(200),default="NULL")
    slug = db.Column(db.String(200),default="NULL")
    created = db.Column(db.Integer, default=0,index=True)
    modified = db.Column(db.Integer, default=0)
    text = db.Column(db.Text, default="NULL")
    order = db.Column(db.Integer, default=0)
    authorId = db.Column(db.Integer, default=0)
    template = db.Column(db.String(32), default="NULL")
    type = db.Column(db.String(16), default="post")
    status = db.Column(db.String(16), default="publish")
    password = db.Column(db.String(32), default="NULL")
    commentsNum = db.Column(db.Integer, default=0)
    allowComment = db.Column(db.Enum,default=0)
    allowPing = db.Column(db.Enum,default=0)
    allowFeed = db.Column(db.Enum,default=0)
    parent = db.Column(db.Integer, default=0)

class aiyblog_fields(db.Model):

    __tablename__ = 'aiyblog_fields'

    cid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200),nullable=False)
    type = db.Column(db.String(8),default="str")
    str_value = db.Column(db.Text,default="NULL")
    int_value = db.Column(db.Integer,default=0)
    float_value = db.Column(db.Float,default=0)


class aiyblog_metas(db.Model):

    __tablename__ = 'aiyblog_metas'

    mid = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    name = db.Column(db.String(200),default="NULL")
    slug = db.Column(db.String(200),default="NULL")
    type = db.Column(db.String(32),nullable=False,default="NULL")
    description = db.Column(db.String(200),default="NULL")
    count = db.Column(db.Integer,default=0)
    order = db.Column(db.Integer,default=0)
    parent = db.Column(db.Integer,default=0)

class aiyblog_options(db.Model):

    __tablename__ = 'aiyblog_options'

    name = db.Column(db.String(32),primary_key=True,nullable=False,default="NULL")
    user = db.Column(db.Integer,nullable=False,default=0)
    value = db.Column(db.Text,default="NULL")

class aiyblog_relationships(db.Model):

    __tablename__ = 'aiyblog_relationships'

    cid = db.Column(db.Integer,nullable=False,default="NULL",primary_key=True)
    mid = db.Column(db.Integer,nullable=False,default="NULL",primary_key=True)

class aiyblog_users(db.Model):

    __tablename__ = 'aiyblog_users'

    uid = db.Column(db.Integer,primary_key=True,nullable=False,default="NULL",autoincrement=True)
    name = db.Column(db.String(32),default="NULL")
    password = db.Column(db.String(64),default="NULL")
    mail = db.Column(db.String(200),default="NULL")
    url = db.Column(db.String(200),default="NULL")
    screenName = db.Column(db.String(200),default="NULL")
    created = db.Column(db.Integer,default=0)
    activated = db.Column(db.Integer,default=0)
    logged = db.Column(db.Integer,default=0)
    group = db.Column(db.String(16),default="visitor")
    authCode = db.Column(db.String(64),default="NULL")

