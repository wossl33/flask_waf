# -*- coding:utf-8 -*-
"""
Flask Waf
---------------
检测针对Flask的恶意攻击请求
"""

from setuptools import setup

setup(
    name='Flask-Waf',
    version='1.0.0',
    url='http://packages.python.org/Flask-Principal/',
    license='MIT',
    author='Hamdell',
    author_email='hamdell@163.com',
    description='web applaction firewall of flask',
    long_description=__doc__,
    py_modules=['flask_waf','rule','engine','thread_pool'],
    zip_safe=False,
    platforms='any',
    package_data={"flask_waf": ["rules/*.json"]},
    install_requires=['Flask'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
