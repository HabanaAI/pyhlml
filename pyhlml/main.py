import ctypes

from pyhlml.hlml_lib import LibHLML

_hlmlOBJ = LibHLML()

def hlmlInit():
    """ 
    Init must be called prior to using any other api function.
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_init")
    ret = fn()

    _hlmlOBJ.inc_ref()
    LibHLML.check_return(ret)
    return None

def hlmlInitWithFlags(flags):
    """
    Init must be called prior to using any other api function.
    Init with flags allows the user to pass an initialization flag. 
    Currently only 0 is supported. 
    """
    global _hlmlOBJ
    
    fn = _hlmlOBJ.get_func_ptr("hlml_init_with_flags")
    ret = fn(flags)

    _hlmlOBJ.inc_ref()
    LibHLML.check_return(ret)
    return None

def hlmlDeviceGetCount():
    """
    Returns the number of AIP devices in the system.
    """
    global _hlmlOBJ 

    count = ctypes.c_uint()
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_count")
    ret = fn(ctypes.byref(count))

    LibHLML.check_return(ret)    
    return count.value

"""



def hlmlShutdown():
    Shutdown should be called last. 
    It properly frees any allocated resources.
    fn = LibHLML.get_func_ptr("hlml_shutdown")
    ret = fn()
    _check_return(ret)
    
    if 0 < LibHLML.ref_count:
        LibHLML.dec_ref()
    
    return None



def hlmlDeviceGetHandleByPCIBusID(pci_addr):
    #Returns the handle for a device from pci_addr info.
    device = HLML_VOID_P.HLML_DEVICE()
    fn = LibHLML.get_func_ptr("hlml_device_get_handle_by_pci_bus_id")


def hlmlDeviceGetHandleByIndex(index):
    fn = LibHLML.get_func_ptr("hlml_device_get_handle_by_index")

def hlmlDeviceGetHandleByUUID(uuid):
    fn = LibHLML.get_func_ptr("hlml_device_get_handle_by_UUID")

def hlmlDeviceGetName(device):

def hlmlDeviceGetPCIInfo(device):

def hlmlDeviceGetClockInfo(device):

def hlmlDeviceGetMaxClockInfo(device):

def hlmlDeviceGetUtilizationRates(device):

def hlmlDeviceGetMemoryInfo(device):

def hlmlDeviceGetTemperature(device, sensor_type):

def hlmlDeviceGetTemperatureThreshold(device, threshold_type):

def hlmlDeviceGetPersistenceMode(device):

def hlmlDeviceGetPerformanceState(device):

def hlmlDeviceGetPowerUsage(device):

def hlmlDeviceGetPowerManagementDefaultLimit(device):

def hlmlDeviceGetECCMode(device):

def hlmlDeviceGetTotalECCErrors(device, error_type, counter_type):

def hlmlDeviceGetUUID(device):

def hlmlDeviceGetMinorNumber(device):

def hlmlDeviceRegisterEvents(device, event_types):

def hlmlEventSetCreate():

def hlmlEventSetFree(set):

def hlmlEventSetWait(set, timeout):

def hlmlDeviceGetMACInfo(device):

def hlmlDeviceERRInject(device):

def hlmlDeviceGetHLRevision(device):

def hlmlDeviceGetPCBInfo(device):

def hlmlDeviceGetSerial(device):

def hlmlDeviceGetBoardID(device):

def hlmlDeviceGetPCIEThroughout(device):

def hlmlDeviceGetPCIEReplayCounter(device):

def hlmlDeviceGetCurrPCIELinkGeneration(device):

def hlmlDeviceGetCurrPCIELinkWidth(device):

def hlmlDeviceGetCurrentClocksThrottleReasons(device):

def hlmlDeviceGetTotalEnergyConsumption(device):

"""