# -*- coding:utf-8 -*-
from flask import Flask,request
from flask_waf import Waf

app=Flask(__name__)
app.config['WAF_MODE']='protection'  # app加载配置文件必须设置WAF_MODE，protection为防护模式；monitor为镜像模式，只记录日志，不拦截防护。
waf=Waf(app)

@app.before_request
# 对HTTP Method禁用
@waf.request_method_forbidden
def befor_request():
    pass

@app.route('/')
# 对url"/"进行WAF过滤，默认规则为"common"，其他选项请参考flask_waf.py文件
@waf.load_waf()
def hello():
    return "hello,world"

@app.route('/upload',methods=['POST'])
# 对url"/upload"的访问进行SQL注入检测
@waf.load_waf("sql_injection")
def upload():
    return "upload ok!"

if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)
