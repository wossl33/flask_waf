# -*- coding:utf-8 -*-
import warnings
from flask import request,config,abort
from functools import wraps
from rule import WafRules
from engine import WafEngine
'''
    WAF运行模式：
        protection:防护模式，拦截并写入日志。
        monitor:镜像模式，不拦截只写入日志。
    说明：
        1、WAF初始化时，必须指定运行模式；app.config['WAF_MODE']='protection。
        2、防护模式和镜像模式只对规则库文件中<status>on</status>的规则起作用。
        
'''

class Waf(object):
    def __init__(self,app=None):
        # 定义Class属性
        if app is not None:
            self.app=app
            self.init_app(self.app)
        else:
            self.app=None

    def setup_app(self,app):
        warnings.warn("Warning setup_app is deprecated.Please use init_app.",DeprecationWarning)

    def init_app(self,app):
        # 加载Flask配置文件中WAF相关配置
        try:
            self.mode=app.config['WAF_MODE']
        except KeyError,e:
            print e
        # 加载规则库
        self.load_waf_rules()
        # 初始化WAF引擎
        self.waf_engine=WafEngine()

    def load_waf_rules(self):
        '''
        加载规则库
        '''
        # 初始化规则库
        self.waf_rules=waf_re=WafRules("rules")
        # 获取禁用HTTP方法
        self._http_forbidden_methods=self.waf_rules.get_json_rules("waf_2017_http_methods_forbidden")
        self._virtual_patching=self.waf_rules.get_json_rules("waf_2017_virtual_patching")
        self._attack_type={
            "common":self.waf_rules.get_json_rules("waf_2017_common"),
            "sql_injection":self.waf_rules.get_json_rules("waf_2017_sql_injection"),
            "xss_attack":self.waf_rules.get_json_rules("waf_2017_xss_attack")
        }

    def waf_mode(self):
        '''
        定义WAF两种模式的处理方式
        '''
        if self.mode == 'protection':
            # abort(404)，拦截并写入日志
            return "waf is running."
        elif self.mode != 'protection' and self.mode == 'monitor':
            # 不拦截写入日志
            pass
        else:
            # 不拦截也不写入日志
            pass

    def request_method_forbidden(self,func):
        '''
        通过app.before_request，对每次的HTTP进行方法检测。若在规则中，则禁用。
        使用方法：
            @app.before_request
            @waf.request_method_forbidden
            def befor_request():
                pass
        '''
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if self._http_forbidden_methods and self.waf_engine.http_method_forbidden(request.method,self._http_forbidden_methods):
                # 发现异常HTTP方法，调用self.waf_mode检测WAF设置模式并响应.
                return self.waf_mode()
            else:
                return func(*args, **kwargs)
        return decorated_view

    def virtual_patching(self,func):
        '''
        通过app.before_request，对每次待检测的请求进行规则匹配，若满足则禁止访问；但是，虚拟规则需自己制定。
        使用方法：
            @app.before_request
            @waf.virtual_patching
            def befor_request():
                pass
        ''' 
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if self._virtual_patching:
                req_arg=[kwargs[i] for i in kwargs]
                if request.method=='GET':
                    req_arg+=[request.args[arg] for arg in request.args]
                    for arg in req_arg:
                        if self.waf_engine.virtual_patching(arg,self._virtual_patching):
                            return self.waf_mode()
                    return func(*args, **kwargs)
                elif request.method=='POST':
                    req_arg+=[request.form[arg] for arg in request.form]
                    for arg in req_arg:
                        if self.waf_engine.virtual_patching(arg,self._virtual_patching):
                            return self.waf_mode()
                    return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
        return decorated_view

    def load_waf(self,attack_type="common"):
        '''
        根据"attack_type"加载对应请求的处理方式，默认是"common".
        '''
        def decarator(func):
            @wraps(func)
            def decorated_view(*args, **kwargs):
                try:
                    rules=self._attack_type[attack_type]
                except KeyError:
                    return func(*args, **kwargs)
                req_arg=[kwargs[i] for i in kwargs]
                if request.method=='GET':
                    req_arg+=[request.args[arg] for arg in request.args]
                    for arg in req_arg:
                        if self.waf_engine.security_check(arg,self._attack_type[attack_type]):
                            return self.waf_mode()
                    return func(*args, **kwargs)
                elif request.method=='POST':
                    req_arg+=[request.form[arg] for arg in request.form]
                    for arg in req_arg:
                        if self.waf_engine.security_check(arg,self._attack_type[attack_type]):
                            return self.waf_mode()
                    return func(*args, **kwargs)
                elif request.method=='HEAD':
                    # 自定义处理方式
                    return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            return decorated_view
        return decarator