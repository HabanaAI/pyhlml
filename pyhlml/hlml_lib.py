import ctypes
import threading

class LibHLML:
    def __init__(self):
        self.lib            = None 
        self.lib_load_lock  = threading.Lock()
        self.func_ptr_cache = dict()
        self.ref_count      = 0 # INC on init DEC on dest
        self._load_lib() 

    def _load_lib(self):
        self.lib_load_lock.acquire()
        try:
            self.lib = ctypes.CDLL("/usr/lib/habanalabs/libhlml.so")
        except Exception as e:
            print(e)
            print("Failed to load libhlml")
        finally:
            self.lib_load_lock.release()
    
    def inc_ref(self):
        self.lib_load_lock.acquire()
        self.ref_count += 1
        self.lib_load_lock.release()
    
    def dec_ref(self):
        if self.ref_count > 0:
            self.lib_load_lock.acquire()
            self.ref_count -= 1
            self.lib_load_lock.release()

    def get_func_ptr(self, name):
        if self.lib == None:
            print("Library not initialized")
        if name in self.func_ptr_cache:
            return self.func_ptr_cache[name]
        self.lib_load_lock.acquire()
        try:
            self.func_ptr_cache[name] = getattr(self.lib, name)
            return self.func_ptr_cache[name]
        finally:
            self.lib_load_lock.release()        

    
