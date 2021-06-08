import ctypes
import string
import threading

from pyhlml.hlml_types import *

class _struct_c_hlml_unit(ctypes.Structure):
    pass # opaque handle

class LibHLML:

    PCI_DOMAIN_LEN                          = 5
    PCI_ADDR_LEN                            = ( PCI_DOMAIN_LEN + 10 )
    PCI_LINK_INFO_LEN                       = 10
    ETHER_ADDR_LEN                          = 6 
    HL_FIELD_MAX_SIZE                       = 32
    HLML_DEVICE_MAC_MAX_ADDRESSES           = 20
    HLML_EVENT_ECC_ERR                      = ( 1 << 0 )
    HLML_EVENT_CRITICAL_ERR                 = ( 1 << 1 )
    HLML_EVENT_CLOCK_RATE                   = ( 1 << 2 )
    HLML_CLOCKS_THROTTLE_REASON_POWER       = ( 1 << 0 )
    HLML_CLOCKS_THROTTLE_REASON_THERMAL     = ( 1 << 1 )

    c_hlml_return                           = ctypes.c_uint
    HLML_SUCCESS                            = 0
    HLML_ERROR_UNINITIALIZED                = 1
    HLML_ERROR_INVALID_ARGUMENT             = 2
    HLML_ERROR_NOT_SUPPORTED                = 3
    HLML_ERROR_ALREADY_INITIALIZED          = 5
    HLML_ERROR_NOT_FOUND                    = 6
    HLML_ERROR_INSUFFICIENT_SIZE            = 7
    HLML_ERROR_DRIVER_NOT_LOADED            = 9
    HLML_ERROR_TIMEOUT                      = 10
    HLML_ERROR_AIP_IS_LOST                  = 15
    HLML_ERROR_MEMORY                       = 20
    HLML_ERROR_NO_DATA                      = 21
    HLML_ERROR_UNKNOWN                      = 49

    c_hlml_clock_type                       = ctypes.c_uint
    HLML_CLOCK_SOC                          = 0
    HLML_CLOCK_IC                           = 1
    HLML_CLOCK_MME                          = 2
    HLML_CLOCK_TPC                          = 3
    HLML_CLOCK_COUNT                        = 4

    c_hlml_temperature_sensors              = ctypes.c_uint
    HLML_TEMPERATURE_ON_AIP                 = 0
    HLML_TEMPERATIRE_ON_BOARD               = 1

    c_hlml_temperature_thresholds           = ctypes.c_uint
    HLML_TEMPERATURE_THRESHOLD_SHUTDOWN     = 0
    HLML_TEMPERATURE_THRESHOLD_SLOWDOWN     = 1
    HLML_TEMPERATURE_THRESHOLD_MEM_MAX      = 2
    HLML_TEMPERATURE_THRESHOLD_GPU_MAX      = 3
    HLML_TEMPERATURE_THRESHOLD_COUNT        = 4

    c_hlml_enable_state                     = ctypes.c_uint
    HLML_FEATURE_DISABLED                   = 0
    HLML_FEATURE_ENABLED                    = 1

    c_hlml_p_states                         = ctypes.c_uint
    HLML_PSTATE_0                           = 0
    HLML_PSTATE_UNKNOWN                     = 3

    c_hlml_memory_error_type                = ctypes.c_uint
    HLML_MEMORY_ERROR_TYPE_CORRECTED        = 0 # NOT SUPPORTED BY HLML
    HLML_MEMORY_ERROR_TYPE_UNCORRECTED      = 1
    HLML_MEMORY_ERROR_TYPE_COUNT            = 2

    c_hlml_ecc_counter_type                 = ctypes.c_uint
    HLML_VOLATILE_ECC                       = 0
    HLML_AGGREGATE_ECC                      = 1
    HLML_ECC_COUNTER_TYPE_COUNT             = 2

    c_hlml_err_inject                       = ctypes.c_uint
    HLML_ERR_INJECT_ENDLESS_COMMAND         = 0
    HLML_ERR_INJECT_NON_FATAL_EVENT         = 1
    HLML_ERR_INJECT_FATAL_EVENT             = 2
    HLML_ERR_INJECT_LOSS_OF_HEARTBEAT       = 3
    HLML_ERR_INJECT_THERMAL_EVENT           = 4
    HLML_ERR_INJECT_COUNT                   = 5

    c_hlml_pcie_util_counter                = ctypes.c_uint
    HLML_PCIE_UTIL_TX_BYTES                 = 0
    HLML_PCIE_UTIL_RX_BYTES                 = 1
    HLML_PCIE_UTIL_COUNT                    = 2
    
    HLML_EVENT_SET                          = ctypes.c_void_p
    HLML_DEVICE                             = ctypes.c_void_p
    #HLML_UNIT                               = ctypes.POINTER(_struct_c_hlml_unit())

    def __init__(self):
        self.lib            = None 
        self.lib_load_lock  = threading.Lock()
        self.func_ptr_cache = dict()
        self.ref_count      = 0 # INC on init DEC on dest
        self._load_lib() 

    def _load_lib(self):
        self.lib_load_lock.acquire()
        try:
            # This is where I'd load windows ... IF I HAD WINDOWS
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

    @classmethod
    def check_return(cls, ret):
        if (ret != LibHLML.HLML_SUCCESS ):
            print(ret)
        return ret

"""
class HLMLError(Exception):
    def _extract_HLML_errors_as_classes():
        '''
        Generates a hierarchy of classes on top of HLMLError class.
        Each HLML Error gets a new HLMLError subclass. This way try,except blocks can filter appropriate
        exceptions more easily.
        HLMLError is a parent class. Each HLML_ERROR_* gets it's own subclass.
        e.g. HLML_ERROR_ALREADY_INITIALIZED will be turned into HLMLError_AlreadyInitialized
        '''
        hlmlErrorsNames = [x for x in dir(c_hlml_return) if x.startswith("HLML_ERROR_")]
        for err_name in hlmlErrorsNames:
            # e.g. Turn HLML_ERROR_ALREADY_INITIALIZED into HLMLError_AlreadyInitialized
            class_name = "HLMLError_" + string.capwords(err_name.replace("HLML_ERROR_", ""), "_").replace("_", "")
            err_val = getattr(c_hlml_return, err_name)
            def gen_new(val):
                def new(typ):
                    obj = HLMLError.__new__(typ, val)
                    return obj
                return new
            new_error_class = type(class_name, (HLMLError,), {'__new__': gen_new(err_val)})
            new_error_class.__module__ = __name__
            setattr(c_hlml_return, class_name, new_error_class)
        return new_error_class

    _classMap = _extract_HLML_errors_as_classes()
    _errcodes = {
        c_hlml_return.HLML_SUCCESS                    : "No error",
        c_hlml_return.HLML_ERROR_UNINITIALIZED        : "Libhlml not initialized",
        c_hlml_return.HLML_ERROR_INVALID_ARGUMENT     : "Invalid argument",
        c_hlml_return.HLML_ERROR_NOT_SUPPORTED        : "Not supported",
        c_hlml_return.HLML_ERROR_ALREADY_INITIALIZED  : "Libhlml already initialized",
        c_hlml_return.HLML_ERROR_NOT_FOUND            : "Not found",
        c_hlml_return.HLML_ERROR_INSUFFICIENT_SIZE    : "Insufficient size",
        c_hlml_return.HLML_ERROR_DRIVER_NOT_LOADED    : "Driver not loaded",
        c_hlml_return.HLML_ERROR_TIMEOUT              : "Timeout",
        c_hlml_return.HLML_ERROR_AIP_IS_LOST          : "AIP Lost",
        c_hlml_return.HLML_ERROR_MEMORY               : "Memory error",
        c_hlml_return.HLML_ERROR_NO_DATA              : "No Data",
        c_hlml_return.HLML_ERROR_UNKNOWN              : "Unknown"
    }

    def __new__(typ, value):
        if typ == HLMLError:
            typ = HLMLError._classMap.get(value, typ)
        obj = Exception.__new__(typ)
        obj.value = value
        return obj
    
    def __str__(self):
        try:
            return HLMLError._errcodes[self.value]
        except HLMLError:
            return f"HLML error with code {self.value}"
    
    def __eq__(self, other):
        return self.value == other.value


def HLML_exception(ec):
    if ec not in HLMLError._classMap:
        raise ValueError(f'hlml error code {ec} is not valid')
    return HLMLError._classMap[ec]

"""