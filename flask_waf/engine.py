# -*- coding:utf-8 -*-
import re
#import thread_pool

class WafEngine(object):
    def __init__(self):
        super(WafEngine,self).__init__()

    # 全局禁用HTTP方法
    def http_method_forbidden(self,request_method,http_forbidden_methods):
        return self.match_rules(request_method,http_forbidden_methods)
    # 虚拟补丁
    def virtual_patching(self,req_arg,rules):
        return self.match_rules(req_arg,rules)

    # 安全检测
    def security_check(self,arg,rules):
        return self.match_rules(arg,rules)

    # 规则匹配处理
    def match_rules(self,arg,rule_queue):
        for i in rule_queue:
            #print i
            if re.search(i,arg,re.IGNORECASE):
                return True
        return False
    

