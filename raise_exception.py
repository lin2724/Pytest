class MyException(Exception):
    pass

try:
    raise MyException({"message":"My hovercraft is full of animals", "animal":"eels"})
except MyException as e:
    details = e.args[0]
    print(details["animal"])
#raise MyException("My hovercraft is full of eels")