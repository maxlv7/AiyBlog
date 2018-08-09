import time

from flask import Blueprint
from flask import url_for,request,redirect,session

from AiyBlog.models import aiyblog_contents,aiyblog_relationships,aiyblog_metas
from AiyBlog import db
from AiyBlog.utils import get_tags_by_cid

action = Blueprint(__name__,"action",url_prefix='/admin/action')

@action.route('/edit-post',methods=["POST"])
def edit_post():
    if request.method == "POST":

        #文章信息
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]


        # 附加信息
        cgs = request.form.getlist("category[]")
        tags = request.form.getlist("tags[]")
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        status = request.form["visibility"]

        #是否有密码
        if request.form["password"]:
            pwd = request.form["password"]
            content = aiyblog_contents(title=title,created=int(time.time()),text=text,type="post",\
                                       status=status,allowComment=allowComments,authorId=session["uid"],password=pwd)
        else:
            content = aiyblog_contents(title=title,created=int(time.time()),text=text,type="post",\
                                       status=status,allowComment=allowComments,authorId=session["uid"])

        db.session.add(content)
        db.session.commit()

        # 先拿到cid,然后再找到对应的mid关系(建立分类关系)
        cid = content.cid
        #用户没有选择分类，那么为默认分类
        if len(cgs)==0:
            relationship = aiyblog_relationships(cid=cid, mid=2)
            t = aiyblog_metas.query.filter_by(mid=2).first()
            t.count += 1
            db.session.add(relationship)
            db.session.add(t)
            db.session.commit()
        else:
            for mid in cgs:
                relationship = aiyblog_relationships(cid=cid,mid=mid)
                #增加count数
                t = aiyblog_metas.query.filter_by(mid=mid).first()
                t.count+=1
                db.session.add(relationship)
                db.session.add(t)
                db.session.commit()

        #建立标签关系
        for mid in tags:
            rea = aiyblog_relationships(cid=cid,mid=int(mid))
            #增加count数
            t = aiyblog_metas.query.filter_by(mid=mid).first()
            t.count+=1
            db.session.add(rea)
            db.session.add(t)
            db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.posts"))


@action.route('/modify-post',methods=["POST"])
def modify_post():
    if request.method == "POST":
        #文章信息
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]

        # 附加信息
        cgs = request.form.getlist("category[]")

        tags = request.form.getlist("tags[]")
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        status = request.form["visibility"]

        #更新文章,但是还要所有数据
        cid = request.form.get("cid")

        new_blog = aiyblog_contents.query.filter_by(cid=int(cid)).first()

        if status == "password":
            pwd = request.form["password"]
            new_blog.password = pwd
        new_blog.title = title
        new_blog.text = text
        new_blog.modified = int(time.time())
        new_blog.status = status
        new_blog.allowComment = allowComments
        new_blog.modified = int(time.time())

        db.session.add(new_blog)
        db.session.commit()

        #删除原来所有的分类(解除分类关系)
        rea = aiyblog_relationships.query.filter_by(cid=cid).all()
        for x in rea:
            t = aiyblog_metas.query.filter_by(mid=x.mid,type="category").first()
            if t!=None:
                t.count-=1
                db.session.add(t)
                db.session.delete(x)
        db.session.commit()

        # 添加
        if len(cgs) == 0:
            relationship = aiyblog_relationships(cid=cid, mid=2)
            t = aiyblog_metas.query.filter_by(mid=2).first()
            t.count+=1
            db.session.add(t)
            db.session.add(relationship)
            db.session.commit()
        else:
            for mid in cgs:
                relationship = aiyblog_relationships(cid=cid, mid=mid)
                t = aiyblog_metas.query.filter_by(mid=mid).first()
                t.count+=1
                db.session.add(relationship)
                db.session.add(t)
            db.session.commit()

        #找到该文章原来所有的标签
        raw_tags = get_tags_by_cid(cid)

        #解除原来所有和标签关系
        for x in raw_tags:
            t = aiyblog_relationships.query.filter_by(mid=x).first()
            db.session.delete(t)
        db.session.commit()

        #count数减一
        for rt in raw_tags:
            t = aiyblog_metas.query.filter_by(mid=rt).first()
            t.count-=1
            db.session.add(t)
        db.session.commit()

        #建立标签关系
        for mid in tags:
            rea = aiyblog_relationships(cid=cid,mid=int(mid))
            #增加count数
            t = aiyblog_metas.query.filter_by(mid=mid).first()
            t.count+=1
            db.session.add(rea)
            db.session.add(t)
        db.session.commit()
        return redirect(url_for("AiyBlog.admin.manage.posts"))


@action.route('/delete-post',methods=["POST"])
def delete_post():

    if request.method == "POST":
        #得到所有文章的cid，是一个list
        cid_list = request.form.getlist("cid[]")
        for cid in cid_list:
            content = aiyblog_contents.query.filter_by(cid=cid).first()
            #解除关联关系
            rea = aiyblog_relationships.query.filter_by(cid=cid).all()
            for x in rea:
                t = aiyblog_metas.query.filter_by(mid=x.mid).first()
                t.count-=1
                db.session.add(t)
                db.session.delete(x)
            #删除内容
            db.session.delete(content)
            #提交
            db.session.commit()
            db.session.close()
        return redirect(url_for("AiyBlog.admin.manage.posts"))

@action.route('/add-page',methods=["POST"])
def add_page():
    if request.method == "POST":
        title = request.form["title"] or "未命名页面"
        slug = request.form["slug"]
        text = request.form["markdown"]
        order = request.form["order"]
        status = request.form["visibility"]
        try:
            allowComments = request.form["allowComments"]
            order = int(order)
        except:
            allowComments = "off"

        if request.form["password"]:
            pwd = request.form["password"]
            page = aiyblog_contents(title=title, slug=slug, text=text, type="page", created=time.time(), status=status, \
                                    allowComment=allowComments, order=order, authorId=session["uid"],password=pwd
                                    )
        else:
            page = aiyblog_contents(title=title,slug=slug,text=text,type="page",created=time.time(),status=status,\
                                allowComment=allowComments,order=order,authorId=session["uid"]
                                )
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("AiyBlog.admin.manage.pages"))

@action.route('/modify-page',methods=["POST"])
def modify_page():
    if request.method == "POST":
        cid = request.form["cid"]
        #先删除原来的
        t = aiyblog_contents.query.filter_by(cid=cid).first()
        created = t.created
        db.session.delete(t)
        db.session.commit()

        title = request.form["title"] or "未命名页面"
        slug = request.form["slug"]
        text = request.form["markdown"]
        order = request.form["order"]
        status = request.form["visibility"]
        try:
            allowComments = request.form["allowComments"]
            order = int(order)
        except:
            allowComments = "off"

        if request.form["password"]:
            pwd = request.form["password"]
            page = aiyblog_contents(cid=cid,title=title, slug=slug, text=text, type="page",created=created,modified=int(time.time()), status=status, \
                                    allowComment=allowComments, order=order, authorId=session["uid"],password=pwd
                                    )
        else:
            page = aiyblog_contents(cid=cid,itle=title, slug=slug, text=text, type="page", created=created,modified=int(time.time()), status=status, \
                                    allowComment=allowComments, order=order, authorId=session["uid"]
                                    )
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("AiyBlog.admin.manage.pages"))

@action.route('/delete-page',methods=["POST"])
def delete_page():
    if request.method == "POST":
        cid_list = request.form.getlist("cid[]")

        for cid in cid_list:
            t = aiyblog_contents.query.filter_by(cid=cid).first()
            db.session.delete(t)
            db.session.commit()
        return redirect(url_for("AiyBlog.admin.manage.pages"))

@action.route('/add-category',methods=["POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"]
        slug = request.form["slug"]
        description = request.form["description"]

        t = aiyblog_metas(name=name,slug=slug,description=description,type="category")
        db.session.add(t)
        db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.categories"))


@action.route('/modify-category',methods=["POST"])
def modify_category():
    if request.method == "POST":
        mid = request.form["mid"]
        name = request.form["name"]
        slug = request.form["slug"]
        description = request.form["description"]

        #修改
        t = aiyblog_metas.query.filter_by(mid=int(mid)).first()
        t.name = name
        t.slug = slug
        t.description = description

        db.session.add(t)
        db.session.commit()
        db.session.close()

        return redirect(url_for("AiyBlog.admin.manage.categories"))

@action.route('/delete-category',methods=["POST"])
def delete_category():
    if request.method == "POST":
        ct_list = request.form.getlist("mid[]")

        #找到该分类对应的所有文章
        cid_list = []
        for ct in ct_list:
            t = aiyblog_relationships.query.filter_by(mid=ct).all()
            for c in t:
                cid_list.append(c.cid)
        # print("cid_list:",set(cid_list))

        cid_list = set(cid_list)

        #找到所有文章中每个文章对应的分类
        mid_list = []
        for cid in cid_list:
            t = aiyblog_relationships.query.filter_by(cid=cid).all()
            for m in t:
                mid_list.append(m.mid)
        # print("mid_list:",mid_list)

        #每个文章对应的分类数减一
        for mid in mid_list:
            t = aiyblog_metas.query.filter_by(mid=mid).first()
            t.count-=1
            db.session.add(t)
            db.session.commit()

        #解除关系(cid-mid)
        for cid in cid_list:
            content = aiyblog_contents.query.filter_by(cid=cid).first()
            #解除关联关系
            rea = aiyblog_relationships.query.filter_by(cid=cid).all()
            for x in rea:
                db.session.delete(x)
                db.session.commit()

        #删除文章
        for cid in cid_list:
            t = aiyblog_contents.query.filter_by(cid=cid).first()
            db.session.delete(t)
            db.session.commit()

        #删除分类
        for mid in ct_list:
            t = aiyblog_metas.query.filter_by(mid=mid).first()
            db.session.delete(t)
            db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.categories"))


@action.route('/add-tag',methods=["POST"])
def add_tag():
    if request.method == "POST":
        name = request.form["name"]
        slug = request.form["slug"]

        tag = aiyblog_metas(name=name,slug=slug,type="tag")

        db.session.add(tag)
        db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.tags"))

@action.route('/modify-tag',methods=["POST"])
def modify_tag():
    if request.method == "POST":
        mid=request.form["mid"]

        name = request.form["name"]
        slug = request.form["slug"]

        tag = aiyblog_metas.query.filter_by(mid=int(mid)).first()

        tag.name = name
        tag.slug = slug

        db.session.add(tag)
        db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.tags"))

@action.route('/delete-tag',methods=["POST"])
def delete_tag():
    if request.method == "POST":
        try:
            mid_list = request.form.getlist("mid[]")
        except:
            pass
        else:
            for mid in mid_list:
                #删除关系
                t = aiyblog_relationships.query.filter_by(mid=mid).all()
                for x in t:
                    db.session.delete(x)
                    db.session.commit()
                #删除标签
                t2 = aiyblog_metas.query.filter_by(mid=mid).first()
                db.session.delete(t2)
                db.session.commit()

        return redirect(url_for("AiyBlog.admin.manage.tags"))

