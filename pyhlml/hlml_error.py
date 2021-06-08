import string

class return_types:
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

def extract_HLML_errors_as_classes():
        '''
        Generates a hierarchy of classes on top of HLMLError class.
        Each HLML Error gets a new HLMLError subclass. This way try,except blocks can filter appropriate
        exceptions more easily.
        HLMLError is a parent class. Each HLML_ERROR_* gets it's own subclass.
        e.g. HLML_ERROR_ALREADY_INITIALIZED will be turned into HLMLError_AlreadyInitialized
        '''
        hlmlErrorsNames = [x for x in dir(return_types) if x.startswith("HLML_ERROR_")]
        for err_name in hlmlErrorsNames:
            # e.g. Turn HLML_ERROR_ALREADY_INITIALIZED into HLMLError_AlreadyInitialized
            class_name = "HLMLError_" + string.capwords(err_name.replace("HLML_ERROR_", ""), "_").replace("_", "")
            err_val = getattr(return_types, err_name)
            def gen_new(val):
                def new(typ):
                    obj = HLMLError.__new__(typ, val)
                    return obj
                return new
            new_error_class = type(class_name, (HLMLError,), {'__new__': gen_new(err_val)})
            new_error_class.__module__ = __name__
            setattr(return_types, class_name, new_error_class)
        return new_error_class

class HLMLError(Exception):
    _classMap = extract_HLML_errors_as_classes()
    _errcodes = {
        return_types.HLML_SUCCESS                    : "No error",
        return_types.HLML_ERROR_UNINITIALIZED        : "Libhlml not initialized",
        return_types.HLML_ERROR_INVALID_ARGUMENT     : "Invalid argument",
        return_types.HLML_ERROR_NOT_SUPPORTED        : "Not supported",
        return_types.HLML_ERROR_ALREADY_INITIALIZED  : "Libhlml already initialized",
        return_types.HLML_ERROR_NOT_FOUND            : "Not found",
        return_types.HLML_ERROR_INSUFFICIENT_SIZE    : "Insufficient size",
        return_types.HLML_ERROR_DRIVER_NOT_LOADED    : "Driver not loaded",
        return_types.HLML_ERROR_TIMEOUT              : "Timeout",
        return_types.HLML_ERROR_AIP_IS_LOST          : "AIP Lost",
        return_types.HLML_ERROR_MEMORY               : "Memory error",
        return_types.HLML_ERROR_NO_DATA              : "No Data",
        return_types.HLML_ERROR_UNKNOWN              : "Unknown"
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