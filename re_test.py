import re
m = re.match(r'(HEAD|TRACE|OPTIONS)', 'HEAD')
print m

if m is not None:
    print "ok"

print 'abc\bdef'
print type(r'abc\bdef')

z = re.match('\\bblow', 'blow')
print z

