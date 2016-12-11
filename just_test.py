# coding=utf-8
hello = u'你好'
not_hello = 'nihao'
print type(hello)
print type(not_hello)
#ret = hello.decode('utf-8')
ret = not_hello.decode('utf-8')
print type(ret)
for i in range(10):
    print i

def methoud(name=None):
    if name:
        print name
    else:
        print 'no name'
methoud(name='hello')