from datetime import datetime
from  fake_useragent import UserAgent
from abc import ABC, abstractmethod
import threading
import time 

# import time
# import threading

class DataClass(ABC):
    '''
    base class:用来限定处理数据步骤
    '''
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
    '''
    时间格式string生成
    '''
    match mode:
        case 0:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}"
        case 1:
            return f"{datetime.today().strftime('%Y%m%d')}"
        case _:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M')}"

def getUserAgent():
    return UserAgent().random

def time_diplayer(func, *args, **kwargs):
    '''
    用来展示消耗时间的工具
    '''
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
    try:
        ret = func(*args, **kwargs)
    except Exception as e:
        ret = None
        pass
    event.set()
    t.join()
    return ret


    
    



