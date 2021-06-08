import ctypes

from pyhlml.libhlml import LibHLML
import pyhlml.hlml_types as hlml_t

_hlmlOBJ = LibHLML()

def hlmlInit() -> None:
    """ 
    Init must be called prior to using any other api function.
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_init")
    ret = fn()

    _hlmlOBJ.inc_ref()
    LibHLML.check_return(ret)
    return None

def hlmlInitWithFlags(flags: int) -> None:
    """
    Init must be called prior to using any other api function.
    Init with flags allows the user to pass an initialization flag. 
    Currently only 0 is supported. 

    Args:
        flags (int) - init flags
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_init_with_flags")
    ret = fn(flags)

    _hlmlOBJ.inc_ref()
    LibHLML.check_return(ret)
    return None

def hlmlShutdown() -> None:
    """
    Shutdown should be called last. 
    It properly frees any allocated resources.
    """
    global _hlmlOBJ 

    fn = _hlmlOBJ.get_func_ptr("hlml_shutdown")
    ret = fn()

    for _ in range(_hlmlOBJ.ref_count):
        _hlmlOBJ.dec_ref()
    LibHLML.check_return(ret)
    return None

def hlmlDeviceGetCount() -> int:
    """
    Returns the number of AIP devices in the system.
    """
    global _hlmlOBJ 
    count = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_count")
    ret = fn(ctypes.byref(count))

    LibHLML.check_return(ret)    
    return count.value

def hlmlDeviceGetHandleByPCIBusID(pci_addr: str) -> LibHLML.HLML_DEVICE():
    """ Acquire the handle for a device, based on PCI Address """
    global _hlmlOBJ

    device = LibHLML.HLML_DEVICE()
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_pci_bus_id")
    ret = fn(pci_addr, ctypes.byref(device))

    LibHLML.check_return(ret)
    return device

def hlmlDeviceGetHandleByIndex(index):
    """ Acquire device handle by index """
    global _hlmlOBJ
    device = LibHLML.HLML_DEVICE()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_index")
    ret = fn(index, ctypes.byref(device))

    LibHLML.check_return(ret)
    return device

def hlmlDeviceGetHandleByUUID(uuid):
    """ Acquire device handle by UUID """
    global _hlmlOBJ
    device = LibHLML.HLML_DEVICE()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_uuid")
    ret = fn(uuid, ctypes.byref(device))

    LibHLML.check_return(ret)
    return device

def hlmlDeviceGetName(device):
    """ Acquire name of device from handle """
    global _hlmlOBJ
    name = ctypes.create_string_buffer(LibHLML.HL_FIELD_MAX_SIZE)

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_name")
    ret = fn(
        device, ctypes.byref(name), ctypes.c_uint(LibHLML.HL_FIELD_MAX_SIZE)
    )

    LibHLML.check_return(ret)
    return device

def hlmlDeviceGetPCIInfo(device):
    """ Get the PCI attributes of input device """
    global _hlmlOBJ
    pci_info = hlml_t.c_hlml_pcb_info()
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pci_info")
    ret = fn(
        device, ctypes.byref(pci_info), ctypes.c_uint(LibHLML.HL_FIELD_MAX_SIZE)
    )

    LibHLML.check_return(ret)
    return device 

def hlmlDeviceGetClockInfo(device):
    """ Get the """

def hlmlDeviceGetMaxClockInfo(device):
    pass

def hlmlDeviceGetUtilizationRates(device):
    pass

def hlmlDeviceGetMemoryInfo(device):
    pass

def hlmlDeviceGetTemperature(device, sensor_type):
    pass

def hlmlDeviceGetTemperatureThreshold(device, threshold_type):
    pass

def hlmlDeviceGetPersistenceMode(device):
    pass

def hlmlDeviceGetPerformanceState(device):
    pass

def hlmlDeviceGetPowerUsage(device):
    pass

def hlmlDeviceGetPowerManagementDefaultLimit(device):
    pass

def hlmlDeviceGetECCMode(device):
    pass

def hlmlDeviceGetTotalECCErrors(device, error_type, counter_type):
    pass

def hlmlDeviceGetUUID(device):
    pass

def hlmlDeviceGetMinorNumber(device):
    pass

def hlmlDeviceRegisterEvents(device, event_types):
    pass

def hlmlEventSetCreate():
    pass

def hlmlEventSetFree(set):
    pass

def hlmlEventSetWait(set, timeout):
    pass

def hlmlDeviceGetMACInfo(device):
    pass

def hlmlDeviceERRInject(device):
    pass

def hlmlDeviceGetHLRevision(device):
    pass

def hlmlDeviceGetPCBInfo(device):
    pass

def hlmlDeviceGetSerial(device):
    pass

def hlmlDeviceGetBoardID(device):
    pass

def hlmlDeviceGetPCIEThroughput(device):
    pass

def hlmlDeviceGetPCIEReplayCounter(device):
    pass

def hlmlDeviceGetCurrPCIELinkGeneration(device):
    pass

def hlmlDeviceGetCurrPCIELinkWidth(device):
    pass

def hlmlDeviceGetCurrentClocksThrottleReasons(device):
    pass

def hlmlDeviceGetTotalEnergyConsumption(device):
    pass