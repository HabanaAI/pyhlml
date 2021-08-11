from string import capwords
from sys import modules

import pyhlml.hlml_types as hlml_t

def ErrorsAsClass():
    this_module = modules[__name__]
    names = [x for x in dir(hlml_t.HLML_RETURN) if x.startswith("HLML_ERROR")]
    for err in names:
        class_name = "HLMLError_" + capwords(err.replace("HLML_ERROR_", ""), "_").replace("_", "")
        err_v = getattr(hlml_t.HLML_RETURN, err)
        def gen_new(val):
            def new(typ):
                obj = HLMLError.__new__(typ, val)
                return obj
            return new
        new_class = type(class_name, (HLMLError,), {'__new__': gen_new(err_v)})
        new_class.__module__ = __name__
        setattr(this_module, class_name, new_class)
        HLMLError._cMap[err_v] = new_class

class HLMLError(Exception):
    _cMap = {}
    _errcodes = {
        hlml_t.HLML_RETURN.HLML_ERROR_UNINITIALIZED        : "Lib not initialized",
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
            typ = HLMLError._cMap.get(value, typ)
        obj = Exception.__new__(typ)
        obj.value = value
        return obj
        
    def __str__(self):
        return f"HLML Error with code {self.value}"

    def __eq__(self, other):
        return self.value == self.other.value