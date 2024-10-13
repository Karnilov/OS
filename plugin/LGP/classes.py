import settings
import threading

def find_shortest_list(tr, cores, target_type):
    indices = [i for i, core in enumerate(cores["8"]) if core[0] == target_type]
    shortest_list = None
    shortest_length = float('inf')
    for index in indices:
        current_list = tr[index]
        if len(current_list) < shortest_length:
            shortest_length = len(current_list)
            shortest_list = index
    return shortest_list

class app:
    def __init__(self):
        self.out=False
        self.tm=False
        self.running=True 
        self.paus=False
        self.func=None
        self.args=[]
        self.kwargs={}
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    def run(self):
        while self.running:
            if not self.paus:
                if self.func!=None:
                    self.func(*self.args,**self.kwargs)
                if self.tm: 
                    self.out=True
                    self.tm=False
    def stop(self):self.running=False
    def timeout(self):self.tm=True
    def answer(self):
        a=self.out
        self.out=False
        return a
    def pause(self):self.paus=True 
    def resume(self):self.paus=False
    def add_func(self,func):self.func=func
    def args(self, *args, **kwargs):
        self.args=args
        self.kwargs=kwargs
    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.running=True 
        self.pause=False
        self.thread.start()
    def ps(self):
        print(self.paus)
    def is_alive(self):return self.thread.is_alive()
    
class core:
    cores=[[],[],[],[],[],[],[],[]]
    def add_process(self, func, type):
        self.cores[find_shortest_list(self.cores, settings.cores,type)].append(func)
    def get_cor(self):
        print(self.cores)
