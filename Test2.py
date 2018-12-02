import threading
import time

class ThreadWorker():
    '''
    The basic idea is given a function create an object.
    The object can then run the function in a thread.
    It provides a wrapper to start it,check its status,and get data out the function.
    '''
    def __init__(self,func):
        self.thread = None
        self.data = None
        self.func = self.save_data(func)

    def save_data(self,func):
        '''modify function to save its returned data'''
        def new_func(*args, **kwargs):
            self.data=func(*args, **kwargs)

        return new_func

    def start(self,params):
        self.data = None
        if self.thread is not None:
            if self.thread.isAlive():
                return 'running' #could raise exception here

        #unless thread exists and is alive start or restart it
        self.thread = threading.Thread(target=self.func,args=params)
        self.thread.start()
        return 'started'

    def status(self):
        if self.thread is None:
            return 'not_started'
        else:
            if self.thread.isAlive():
                return 'running'
            else:
                return 'finished'

    def get_results(self):
        if self.thread is None:
            return 'not_started' #could return exception
        else:
            if self.thread.isAlive():
                return 'running'
            else:
                return self.data

def add(x,y):
    time.sleep(x/10)
    return x*y

t = []
for x in range(10):        
    th = ThreadWorker(add)
    th.start((x,'Hi'))
    t.append(th)

# wait until the thread terminates.

while True:
    finish = 0
    for x in range(10):
        if t[x].status() == 'finished':
            finish+= 1
        else:
            print('waiting')
            break
    if finish == 10:
        break

for x in range(10):
    print(t[x].get_results())
       
'''
add1_worker = ThreadWorker(add)
add1_worker.start((1,2))

add2_worker = ThreadWorker(add)
add2_worker.start((2,2))

add3_worker = ThreadWorker(add)
add3_worker.start((5,2))

while True:
    if add1_worker.status() == 'finished' and add2_worker.status() == 'finished' and add3_worker.status() == 'finished':
        break
    else:
        print('waiting')
print (add1_worker.get_results(), add2_worker.get_results(), add3_worker.get_results())
'''
