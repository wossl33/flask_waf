Flask-Waf
=========================

1.0.0
-------------
1、实现WAF插件的防护和旁路模式。

2、调用app.before_request实现全局性的HTTP METHOD禁用。

3、实现了WAF应用层的虚拟补丁，自定义规则。

4、通过向load_waf传入参数，每个路由根据自身需求添加防护规则。

5、对GET方法的url参数和kwargs进行检测，以及POST方法的form参数和kwargs进行检测。


下个版本实现：

1、攻击日志的归档

2、jinja2注入的检测

3、上传内容的WebShell检查

4、cookie检测
