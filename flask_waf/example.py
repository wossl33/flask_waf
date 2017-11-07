from flask import Flask,request
from flask_waf import Waf

app=Flask(__name__)
app.config['WAF_MODE']='protection'
waf=Waf(app)

@app.before_request
@waf.request_method_forbidden
def befor_request():
    pass

@app.route('/')
@waf.load_waf()
def hello():
    return "hello,world"

@app.route('/upload',methods=['POST'])
@waf.load_waf()
def upload():
    print request.form.get('a')
    return "ok"

if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)