"""
负责视图和路由
"""
import hashlib

from flask import request
from flask import jsonify
from flask import redirect
from flask import render_template,make_response

from . import main_blueprint
from APP import csrf
from APP.models import *
from flask import session
from .forms import TeacherForm
# from APP import cache

import functools
def loginValid(fun):
    @functools.wraps(fun)
    def inner(*args,**kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("user_id")
        session_username = session.get("username")
        if username and id and session_username:
            if username == session_username:
                return fun(*args,**kwargs)
        return redirect("/login/")
    return inner

def setPassword(password):
    #password += BaseConfig.SECRET_KEY
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()
@csrf.exempt
@main_blueprint.route("/register/",methods=["GET","POST"])
def register():
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity = form_data.get("identity")
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identity = int(identity)
        user.save()
        return redirect("/login/")
    return render_template("/register.html", **locals())


# def gin():
#     if request.method == "POST":
#         form_data = request.form
#         username = form_data.get("username")
#         password = form_data.get("password")
#
#         user = User.query.filter_by(username = username).first()
#         if user:
#             send_password = setPassword(password)
#             db_password = user.password
#             if send_password == db_password:
#                 # 进行跳转
#                 response = redirect("/index/")
#                 #设置cookie
#                 response.set_cookie("username",username)
#                 response.set_cookie("user_id",str(user.id))
#                 #设置session
#                 session["username"] = username
#                 #返回跳转
#                 return response
#     return render_template("login.html", **locals())
@csrf.exempt
@main_blueprint.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        print("this is post")
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")

        #获取用户信息
        user = User.query.filter_by(username = username).first()
        #检查是老师还是学生
        identity = user.identity
        #检查身份资料是否完善
        identity_id = user.identity_id
        if user:
            send_password = setPassword(password)
            db_password = user.password
            if send_password == db_password:
                # 进行跳转
                response = redirect("/index/")
                #设置cookie
                response.set_cookie("username",username)
                response.set_cookie("user_id",str(user.id))
                #用户是老师还是学员
                response.set_cookie("identity", str(identity) )
                #用cookie判断是否完善了身份
                if identity_id:
                    response.set_cookie("identity_id", str(identity_id))
                else:
                    response.set_cookie("identity_id", "")
                #设置session
                session["username"] = username
                #返回跳转
                return response
    return render_template("login.html", **locals())
@csrf.exempt
@main_blueprint.route("/index/",methods=["GET","POST"])
# @cache.cached(timeout=30,key_prefix="index")
@loginValid
def index():
    identity=request.cookies.get("identity")
    if identity and identity=="1":
        teacher_id = request.cookies.get("identity_id")
        if teacher_id:
            teachers = Teachers.query.get(int(teacher_id))
        else:
            teachers = {}
        if request.method == "POST":
            username = request.form.get("username")
            age = request.form.get("age")
            gender = request.form.get("gender")
            course = request.form.get("course")
                #保存教师的详细信息
            teachers = Teachers()
            teachers.name = username
            teachers.age = age
            teachers.gender = gender
            teachers.course_id = int(course)
            teachers.save()
            #更新用户和教师关联
            user = User.query.get(int(request.cookies.get("user_id")))
            user.identity_id = teachers.id
            user.save()
            #将用户的详情信息的状态修改掉
            response = make_response(render_template("index.html", **locals()))
            # print(type(response))
            response.set_cookie("identity_id", str(teachers.id))
            return response
    elif identity and identity=="0":
        student_id = request.cookies.get("identity_id")
        if student_id:
            students = Students.query.get(int(student_id))
        else:
            students = {}
        if request.method == "POST":
            username = request.form.get("username")
            age = request.form.get("age")
            gender = request.form.get("gender")
            course = request.form.get("course")
            # 保存教师的详细信息
            students = Students()
            students.name = username
            students.age = age
            students.gender = gender
            students.save()
            # 更新用户和教师关联
            user = User.query.get(int(request.cookies.get("user_id")))
            user.identity_id = students.id
            user.save()
            response = make_response(render_template("index.html", **locals()))
            # print(type(response))
            response.set_cookie("identity_id", str(student_id))
            return response
    return render_template("index.html", **locals())
@csrf.exempt
@main_blueprint.route("/logout/",methods=["GET","POST"])
def logout():
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
    del session["username"]
    return response

@csrf.exempt
@main_blueprint.route("/student_list/",methods=["GET","POST"])
def student_list():
    students = Students.query.all()
    response = render_template("students_list.html", **locals())
    #response.set_cookie("")
    return response

@csrf.exempt
@main_blueprint.route("/add_teacher/",methods=["GET","POST"])
def add_teacher():
    teacher_form = TeacherForm()
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")

        t = Teachers()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = int(course)
        t.save()
    return render_template("add_teacher.html",**locals())

@csrf.error_handler
# @app.errorhandler(CSRFError)
@main_blueprint.route("/csrf_403/")
def csrf_token_error(reason):
    print(reason) #错误信息 #The CSRF token is missing.
    return render_template("csrf_403.html",**locals())


@main_blueprint.route("/userValid/",methods=["GET","POST"])
def UserValid():
    result = {
        "code":"",
        "data":""
    }
    if request.method == "POST":
        data = request.form.get("username")
        if data:
            user = User.query.filter_by(username = data).first()
            if user:
                result["code"] = 400
                result["data"] = "用户名已经存在"
            else:
                result["code"] = 200
                result["data"] = "用户名未被注册，可以使用"
    else:
        result["code"] = 400
        result["data"] = "请求方式错误"
    return jsonify(result)



# @app.route("/userValid/")
# def UserValid():
#     result = {
#         "code":"",
#         "data":""
#     }
#     data = request.args.get("username")
#     if data:
#         user = User.query.filter_by(username = data).first()
#         if user:
#             result["code"] = 400
#             result["data"] = "用户名已经存在"
#         else:
#             result["code"] = 200
#             result["data"] = "用户名未被注册，可以使用"
#     return jsonify(result)


#csrf.exempt 单视图函数避免csrf校验
#csrf.error_headler 重新定义403错误页