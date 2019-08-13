#生成器
# def hello():
#     for i in (1,99,3):
#         key = yield i
#         print(key)
#         print("hello world")
#
# h = hello()
# print("++++++++++++++++++++++++++++++++++++++++")
# print(next(h))#1
# print("++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
# print("++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
#send方法
# print("++++++++++++++++++++++++++++++++++++++++")
# print(next(h))#1
# print("++++++++++++++++++++++++++++++++++++++++")
# print(h.send(10))# 10 helloworld
# print("++++++++++++++++++++++++++++++++++++++++")
# print(h.send(20))#20 helloworld
# print("++++++++++++++++++++++++++++++++++++++++")

#在实际工作当中，协程至少需要两个函数
# def getContent():
#     """
#     获取内容的方法
#     """
# def getContent():
#     while True:
#         url = yield "I have content"
#         print("get content from url:%s"%url)
# def getUrl(g):
#     url_list = ["url1","url2","url3","url4","url5"]
#     for i in url_list:
#          print("+++++++++++++++++++++++++++++++++++++")
#          g.send(i)
#          print("+++++++++++++++++++++++++++++++++++++")
#
# if __name__ == "__main__":
#     g = getContent()
#     print(next(g))
#     getUrl(g)
#https://blog.csdn.net/u014331598/article/details/84622652
import gevent
# def fun1():
#     for i in range(5):
#         print("I am fun 1 this is %s"%i)
#         gevent.sleep(0)
# def fun2():
#     for i in range(5):
#         print("I am fun 2 this is %s"%i)
#         gevent.sleep(0)
# # fun1()
# # fun2()
# t1 = gevent.spawn(fun1)
# t2 = gevent.spawn(fun2)
# gevent.joinall([t1,t2])
import gevent
from gevent.lock import Semaphore
sem = Semaphore(1)
def fun1():
    for i in range(5):
        sem.acquire()
        print("I am fun 1 this is %s"%i)
        sem.release()
def fun2():
    for i in range(5):
        sem.acquire()
        print("I am fun 2 this is %s"%i)
        sem.release()
# fun1()
# fun2()
t1 = gevent.spawn(fun1)
t2 = gevent.spawn(fun2)
gevent.joinall([t1,t2])