from datetime import datetime
from  fake_useragent import UserAgent
from abc import ABC, abstractmethod

import threading
import time 

class DataClass(ABC):
    def __init__(self,headers=None):
        # self._url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {"User-Agent":getUserAgent()} 
    @abstractmethod
    def get_data_json(self,*args,**kwargs):
        pass
    
    def get_data_df(self,*args,**kwargs):
        pass


def getStrDate(mode):
    match mode:
        case 0:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}"
        case 1:
            return f"{datetime.today().strftime('%Y%m%d')}"
        case _:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M')}"


def getUserAgent():
    return UserAgent().random


import time
import threading

def time_diplayer(func, *args, **kwargs):
    event = threading.Event()
    s = time.time()
    def timer(event,s):
        try:
            while not event.is_set():
                # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                current_time = str(round(time.time() -s,3)) 
                print("\r" + current_time + " s", end='', flush=True)
                time.sleep(1)
        except Exception as e:
            raise e
    
    t = threading.Thread(target=timer, args=(event,s))
    t.start()
    
    ret = func(*args, **kwargs)
    
    event.set()
    t.join()
    return ret


    
    



