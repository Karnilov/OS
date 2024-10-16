import settings.core as settings
import threading
import time

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
    time=0
    is_alive=False
    time=0
    pause=False
    stop=False
    
    def __init__(self):
        self.tread=threading.Thread(target=self.work, daemon=True)
        
    def work(self):
        while not self.stop:
            if not self.pause:
                t1=time.time_ns()
                self.Cycle()
                t2=time.time_ns()
                self.is_alive=True
                self.time=t2-t1
                    
    def Cycle(self):
        pass
        
    def start(self):
        self.tread.start()
        self.stop=False
    def join(self):self.tread.join()
    def timeout(self): return self.time
    def answer(self): return self.is_alive
    def terminate(self):self.stop=True
    
    
class core:
    cores=[[],[],[],[],[],[],[],[]]
    def add_process(self, func, type):
        self.cores[find_shortest_list(self.cores, settings.cores,type)].append(func)
    def get_cor(self):
        print(self.cores)
    def kill(self,CID, PID):
        self.cores[CID][PID].terminate()
        del self.cores[CID][PID]

class scc:
    def __init__(self,core):
        self.core=core
        self.millis=20
    def regulation(self):
        max=0
        while True:
            for cores_index, cores_ in enumerate(self.core.cores):
                for core_index, core_ in enumerate(cores_):
                    t=core_.timeout()/1000000
                    if t>self.millis:
                        self.core.kill(cores_index,core_index)
