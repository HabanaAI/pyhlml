import string
import sys

import pyhlml.hlml_types as hlml_t

class HLMLError(Exception):
    
    _classMap = extract_HLML_errors_as_classes()
    _errcodes = {
        hlml_t.HLML_RETURN.HLML_SUCCESS                    : "No error",
        hlml_t.HLML_RETURN.HLML_ERROR_UNINITIALIZED        : "Libhlml not initialized",
        hlml_t.HLML_RETURN.HLML_ERROR_INVALID_ARGUMENT     : "Invalid argument",
        hlml_t.HLML_RETURN.HLML_ERROR_NOT_SUPPORTED        : "Not supported",
        hlml_t.HLML_RETURN.HLML_ERROR_ALREADY_INITIALIZED  : "Libhlml already initialized",
        hlml_t.HLML_RETURN.HLML_ERROR_NOT_FOUND            : "Not found",
        hlml_t.HLML_RETURN.HLML_ERROR_INSUFFICIENT_SIZE    : "Insufficient size",
        hlml_t.HLML_RETURN.HLML_ERROR_DRIVER_NOT_LOADED    : "Driver not loaded",
        hlml_t.HLML_RETURN.HLML_ERROR_TIMEOUT              : "Timeout",
        hlml_t.HLML_RETURN.HLML_ERROR_AIP_IS_LOST          : "AIP Lost",
        hlml_t.HLML_RETURN.HLML_ERROR_MEMORY               : "Memory error",
        hlml_t.HLML_RETURN.HLML_ERROR_NO_DATA              : "No Data",
        hlml_t.HLML_RETURN.HLML_ERROR_UNKNOWN              : "Unknown"
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


def extract_HLML_errors_as_classes():
        '''
        Generates a hierarchy of classes on top of HLMLError class.
        Each HLML Error gets a new HLMLError subclass. This way try,except blocks can filter appropriate
        exceptions more easily.
        HLMLError is a parent class. Each HLML_ERROR_* gets it's own subclass.
        e.g. HLML_ERROR_ALREADY_INITIALIZED will be turned into HLMLError_AlreadyInitialized
        '''
        hlmlErrorsNames = [x for x in dir(hlml_t.HLML_RETURN) if x.startswith("HLML_ERROR_")]
        for err_name in hlmlErrorsNames:
            # e.g. Turn HLML_ERROR_ALREADY_INITIALIZED into HLMLError_AlreadyInitialized
            class_name = "HLMLError_" + string.capwords(err_name.replace("HLML_ERROR_", ""), "_").replace("_", "")
            err_val = getattr(hlml_t.HLML_RETURN, err_name)
            def gen_new(val):
                def new(typ):
                    obj = HLMLError.__new__(typ, val)
                    return obj
                return new
            new_error_class = type(class_name, (HLMLError,), {'__new__': gen_new(err_val)})
            new_error_class.__module__ = __name__
            setattr(HLMLError, class_name, new_error_class)
        return new_error_class
