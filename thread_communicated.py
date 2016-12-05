import multiprocessing

from multiprocessing import Process, Pipe


def f(conn):
    for i in range(10):
        conn.send([42, None, 'hello'])
    conn.send('quit')
    conn.close()


def get_message(index, con):
    while True:
        tmp = con.recv()   # prints "[42, None, 'hello']"
        if type(tmp) == str and tmp == 'quit':
            print "done id:%d" % index
            break
        print tmp
    pass

"""
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    while True:
        tmp = parent_conn.recv()   # prints "[42, None, 'hello']"
        if type(tmp) == str and tmp == 'quit':
            print "done"
            break
        print tmp
    p.join()
"""

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=get_message, args=(1, child_conn,))
    p.start()
    p = Process(target=get_message, args=(2, child_conn,))
    p.start()
    p = Process(target=get_message, args=(3, child_conn,))
    p.start()
    for i in range(20):
        parent_conn.send([i, None, 'hello'])
    for i in range(4):
        parent_conn.send('quit')
    p.join()