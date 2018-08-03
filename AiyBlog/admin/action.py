import time

from flask import Blueprint
from flask import url_for,request,redirect,session

from AiyBlog.models import aiyblog_contents,aiyblog_relationships,aiyblog_metas
from AiyBlog import db

action = Blueprint(__name__,"action",url_prefix='/admin/action')

@action.route('/edit-post',methods=["POST"])
def edit_post():
    if request.method == "POST":

        #文章信息
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]


        # 附加信息
        cgs = request.form.getlist("category[]")
        raw_tags = request.form["tags"]
        new_tags = raw_tags.replace('，',',').split(',')
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        status = request.form["visibility"]

        # some oper
        content = aiyblog_contents(title=title,created=int(time.time()),text=text,type="post",\
                                   status=status,allowComment=allowComments,authorId=session["uid"])
        db.session.add(content)
        db.session.commit()

        # 先拿到cid,然后再找到对应的mid关系
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

        return redirect(url_for("AiyBlog.admin.manage.posts"))


@action.route('/modify-post',methods=["POST"])
def modify_post():
    if request.method == "POST":
        #文章信息
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]

        # 附加信息
        cgs = request.form.getlist("category[]")
        raw_tags = request.form["tags"]
        new_tags = raw_tags.replace('，',',').split(',')
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        status = request.form["visibility"]

        #更新文章,但是还要所有数据
        cid = request.form.get("cid")

        new_blog = aiyblog_contents.query.filter_by(cid=int(cid)).first()
        new_blog.title = title
        new_blog.text = text
        new_blog.modified = int(time.time())
        new_blog.status = status
        new_blog.allowComments = allowComments

        db.session.add(new_blog)
        db.session.commit()

        #删除原来所有的分类(解除分类关系)
        rea = aiyblog_relationships.query.filter_by(cid=cid).all()
        for x in rea:
            t = aiyblog_metas.query.filter_by(mid=x.mid).first()
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
                db.session.delete(x)
            #删除内容
            db.session.delete(content)
            #提交
            db.session.commit()
            db.session.close()
        return redirect(url_for("AiyBlog.admin.manage.posts"))


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

        # 先删除分类
        for mid in ct_list:
            t = aiyblog_metas.query.filter_by(mid=mid).first()
            db.session.delete(t)

        #删除分类，解除与文章的关联，删除该分类下所有的内容
        print("t.count is %d"%(t.count))
        if t.count != 0:
            #解除与文章的关联
            cid_list = list()
            for mid in ct_list:
                t = aiyblog_relationships.query.filter_by(mid=mid).first()
                cid_list.append(t.cid)
                db.session.delete(t)
            #删除内容
            for cid in cid_list:
                t = aiyblog_contents.query.filter_by(cid=cid).first()
                db.session.delete(t)

        db.session.commit()
        db.session.close()

        return redirect(url_for("AiyBlog.admin.manage.categories"))
