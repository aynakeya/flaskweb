from app import app
from flask import jsonify,request,render_template,url_for,make_response
import datetime
import mysql.connector
import json

from app.api import database

codes = {"-1":"传入参数错误",
         "-2":"请求方式不支持",
         "-3":"服务器内部错误",
         "1":"登陆成功",
         "2":"用户名不存在",
         "3":"密码错误",
         "4":"注册成功",
         "5":"用户名已存在",
         "6":"信息获取成功",
         "7":"该用户不存在",
         "8":"成功获取用户信息",
         "9":"成功登出",
         "10":"你还没登陆呢"}


def newjson(code,data = ""):
    return jsonify({"code":code,"message":codes[code],"data":data})

from app.api import login
from app.api import register
from app.api import getmsg
from app.api import logout
