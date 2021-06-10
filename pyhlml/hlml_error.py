import string
import sys

import pyhlml.hlml_types as hlml_t

class HLMLError(Exception):

    _errcodes = {
        hlml_t.HLML_RETURN.HLML_SUCCESS                    : "No error",
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

    def __init__(self, status_code):
        self.status_code = status_code
        
        if status_code in HLMLError._errcodes:
            print(HLMLError._errcodes[status_code])
        else:
            raise HLMLError(hlml_t.HLML_RETURN.HLML_ERROR_UNKNOWN)
        
    
    def __str__(self):
        try:
            return HLMLError._errcodes[self.status_code]
        except HLMLError:
            return f"HLML error with code {self.status_code}"
            