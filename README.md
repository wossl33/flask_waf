# flask_waf
web application firewall of flask

Flask框架应用防火墙插件，针对SQL注入和XSS攻击，用来做学习测试。


1、实现WAF插件的防护和旁路模式。

2、调用app.before_request实现全局性的HTTP METHOD禁用。

3、实现了WAF应用层的虚拟补丁，自定义规则。

4、通过向load_waf传入参数，每个路由根据自身需求添加防护规则。

5、对GET方法的url参数和kwargs进行检测，以及POST方法的form参数和kwargs进行检测。


使用方法：
    请参考test.py
    
来源：https://github.com/hamdell/flask_waf.git
