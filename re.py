import re

test_string = 'hello world ,zzl'
m = re.search('zxl', test_string)
if m:
    print m.group(0)
else:
    print 'not found'
