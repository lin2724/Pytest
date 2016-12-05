import thread
import multiprocessing
import time

def thread_child(dly):
    for i in range(10):
        print "child count %d" % i
        time.sleep(dly)
    print "terminated"
    pass


if __name__=="__main__":
    p1 = multiprocessing.Process(target=thread_child, args=(2,))
    p2 = multiprocessing.Process(target=thread_child, args=(1,))
    p1.start()
    p2.start()
    pass
