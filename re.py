import re

test_string = 'hello world ,zzl'
# (?P<first_name>\w+)
m = re.search('zxl', test_string)
if m:
    print m.group(0)
else:
    print 'not found'
