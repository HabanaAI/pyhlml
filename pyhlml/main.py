import ctypes

from sys import modules

import pyhlml.hlml_types as hlml_t

from pyhlml.hlml_lib import LibHLML
from pyhlml.hlml_error import HLMLError, ErrorsAsClass

_hlmlOBJ = None

def _wrapperInit():
    """ init module level object and error classes """
    ErrorsAsClass()
    setattr(modules[__name__], "_hlmlOBJ", LibHLML())

def check_return(ret):
        if (ret != hlml_t.HLML_RETURN.HLML_SUCCESS ):
            HLMLError(ret)
        return ret

def hlmlInit() -> None:
    """ Must be called before any other api can be used
        Parameters: None
        Returns: None
    """
    _wrapperInit()
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_init")
    ret = fn()

    _hlmlOBJ.inc_ref()
    check_return(ret)
    return None

def hlmlInitWithFlags(flags=0) -> None:
    """ Allows the user to call the init function with a flag.
        Parameters:
            flags (int) [ default=0 ] - only the default is supported
        Returns: None
    """
    _wrapperInit()
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_init_with_flags")
    ret = fn(flags)

    _hlmlOBJ.inc_ref()
    check_return(ret)
    return None

def hlmlShutdown() -> None:
    """ Shutdown should be called last.
        Parameters: None
        Returns: None
    """
    global _hlmlOBJ 

    fn = _hlmlOBJ.get_func_ptr("hlml_shutdown")
    ret = fn()

    for _ in range(_hlmlOBJ.ref_count):
        _hlmlOBJ.dec_ref()
    check_return(ret)
    return None

def hlmlDeviceGetCount() -> int:
    """ Returns the number of Habana devices in the system.
        Parameters: None
        Returns:
            count (int) - Number of habana devices. 
                          Ex. An HLS1-H would return 4
    """
    global _hlmlOBJ 
    count = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_count")
    ret = fn(ctypes.byref(count))

    check_return(ret)    
    return count.value

def hlmlDeviceGetHandleByPCIBusID(pci_addr: str) -> hlml_t.HLML_DEVICE.TYPE:
    """ Acquire the handle for a device, based on PCI Address 
        Parameters
    """
    global _hlmlOBJ

    device = hlml_t.HLML_DEVICE.TYPE
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_pci_bus_id")
    ret = fn(str.encode(pci_addr), ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetHandleByIndex(index: int) -> hlml_t.HLML_DEVICE.TYPE:
    """ Acquire device handle by index """
    global _hlmlOBJ
    device = hlml_t.HLML_DEVICE.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_index")
    ret = fn(index, ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetHandleByUUID(uuid: str) -> hlml_t.HLML_DEVICE.TYPE:
    """ Acquire device handle by UUID """
    global _hlmlOBJ
    device = hlml_t.HLML_DEVICE.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_UUID")
    ret = fn(str.encode(uuid), ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetName(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Acquire name of device from handle """
    global _hlmlOBJ
    name = ctypes.create_string_buffer(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_name")
    ret = fn(
        device, ctypes.byref(name), 
        ctypes.c_uint(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)
    )

    check_return(ret)
    return name.value

def hlmlDeviceGetPCIInfo(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.c_hlml_pci_info:
    """ Get the PCI attributes of input device """
    global _hlmlOBJ
    pci_info = hlml_t.c_hlml_pci_info()
    
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pci_info")
    ret = fn(
        device, ctypes.byref(pci_info), 
        ctypes.c_uint(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)
    )

    check_return(ret)
    return pci_info

def hlmlDeviceGetClockInfo(device: hlml_t.HLML_DEVICE.TYPE, clock_type=0 ) -> int:
    """ Retrives the current speed of the selected clock (MHz)
        clock_type ( 0-SOC ( GAUDI ) / 1-IC ( GOYA ) / 2-MME ( GOYA ) / 3-TPC ( GOYA ) )
    """
    global _hlmlOBJ
    speed = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_clock_info")
    ret = fn(device, clock_type, ctypes.byref(speed))

    check_return(ret)
    return speed.value

def hlmlDeviceGetMaxClockInfo(device: hlml_t.HLML_DEVICE.TYPE, clock_type=0 ) -> int:
    """ Retrives the maximum speed of the selected clock (MHz)
        clock_type ( 0-SOC ( GAUDI ) / 1-IC ( GOYA ) / 2-MME ( GOYA ) / 3-TPC ( GOYA ) )
    """
    global _hlmlOBJ
    speed = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_max_clock_info")
    ret = fn(device, clock_type, ctypes.byref(speed))

    check_return(ret)
    return speed.value 

def hlmlDeviceGetUtilizationRates(device: hlml_t.HLML_DEVICE.TYPE) -> int: 
    """ Returns utilization over the past second as a percentage """
    global _hlmlOBJ
    hlml_util = hlml_t.c_hlml_utilization()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_utilization_rates")
    ret = fn(device, ctypes.byref(hlml_util))

    check_return(ret)
    return hlml_util.aip

def hlmlDeviceGetMemoryInfo(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.c_hlml_memory:
    """ Returns the total, used, and free memory in bytes"""
    global _hlmlOBJ
    hlml_mem = hlml_t.c_hlml_memory()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_memory_info")
    ret = fn(device, ctypes.byref(hlml_mem))

    check_return(ret)
    return hlml_mem

def hlmlDeviceGetTemperature(
        device: hlml_t.HLML_DEVICE.TYPE, sensor_type: hlml_t.HLML_TEMP_SENS.TYPE
    ) -> int:
    """ Retrives the current temperature (celsius) of the selected sensor_type 
        sensor_types ( 0-AIP / 1-BOARD )
    """
    global _hlmlOBJ
    temp = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_temperature")
    ret = fn(device, sensor_type, ctypes.byref(temp))

    check_return(ret)
    return temp.value

def hlmlDeviceGetTemperatureThreshold(device: hlml_t.HLML_DEVICE.TYPE, threshold_type: int) -> int:
    """ Retrieves the known temperature (celsius) threshold of the requested type 
        threshold_type (0-shutdown / 1-slowdown / 2-memory / 3-gpu )
    """
    global _hlmlOBJ
    temp = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_temperature_threshold")
    ret = fn(device, threshold_type, ctypes.byref(temp))

    check_return(ret)
    return temp.value

def hlmlDeviceGetPowerUsage(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves power usage for the device in mW """
    global _hlmlOBJ
    power = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_power_usage")
    ret = fn(device, ctypes.byref(power))

    check_return(ret)
    return power.value

def hlmlDeviceGetPowerManagementDefaultLimit(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves default power management limit on this device in mW """
    global _hlmlOBJ
    power = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_power_management_default_limit")
    ret = fn(device, ctypes.byref(power))

    check_return(ret)
    return power

def hlmlDeviceGetECCMode(device: hlml_t.HLML_DEVICE.TYPE) -> dict:
    """ Retrieves the current and pending ECC modes of the device """
    global _hlmlOBJ
    current = ctypes.c_uint()
    pending = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_ecc_mode")
    ret = fn(device, ctypes.byref(current), ctypes.byref(pending))

    return { "current": current.value, "pending": pending.value }

def hlmlDeviceGetTotalECCErrors(
    device: hlml_t.HLML_DEVICE.TYPE, error_type: hlml_t.HLML_MEMORY_ERROR.TYPE, 
    counter_type: hlml_t.HLML_ECC_COUNTER
    ) -> int:
    """ Returns the number of ECC errors for a device. Number is from the last reset, or driver
        reinstall. Currently only the number of corrected errors is supported.
        error_type ( 0-CORRECTED / 1-UNCORRECTED )
        counter_type ( 0-VOLATILE / 1-AGGREGATE )
    """
    global _hlmlOBJ
    count = ctypes.c_longlong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_total_ecc_errors")
    ret = fn(device, error_type, counter_type, ctypes.byref(count))

    check_return(ret)
    return count.value

def hlmlDeviceGetUUID(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Returns the UUID of the device """
    global _hlmlOBJ
    name = ctypes.create_string_buffer(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)
    
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_uuid")
    ret = fn(device, ctypes.byref(name), hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)

    check_return(ret)
    return name

def hlmlDeviceGetMinorNumber(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the minor number of the device ( maps to the device node file )
        at /sys/class/habanalabs/hl[minor]
    """
    global _hlmlOBJ
    number = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_minor_number")
    ret = fn(device, ctypes.byref(number))

    check_return(ret)
    return number

def hlmlEventSetCreate() -> hlml_t.HLML_EVENT_SET.TYPE:
    """ Create an empty set of events """
    global _hlmlOBJ
    st = hlml_t.HLML_EVENT_SET.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_event_set_create")
    ret = fn(ctypes.byref(st))

    check_return(ret)
    return st

def hlmlEventSetFree(st: hlml_t.HLML_EVENT_SET.TYPE) -> None:
    """ Release a set of events """
    global _hlmlOBJ
    
    fn = _hlmlOBJ.get_func_ptr("hlml_event_set_free")
    ret = fn(st)

    check_return(ret)
    return None

def hlmlDeviceRegisterEvents(
        device: hlml_t.HLML_DEVICE.TYPE, event_types: int, 
        st: hlml_t.HLML_EVENT_SET.TYPE
    ) -> None:
    """ Start recording events on input device add events to input set
        event_types ( 0-ECC_err / 1-Crit_err / 2-Clock_change ) 
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_device_register_events")
    ret = fn(device, event_types, st)

    check_return(ret)
    return None

def hlmlEventSetWait(st: hlml_t.HLML_EVENT_SET.TYPE, timeout: int) -> hlml_t.c_hlml_event_data:
    """ Waits on events and delivers events. 
        If some events are ready to be delivered at the time of the call, function returns immediately.
        If there are no events ready to be delivered, function sleeps until the event arrives but not longer than the specified timeout.
    """
    global _hlmlOBJ
    data = hlml_t.c_hlml_event_data()

    fn = _hlmlOBJ.get_func_ptr("hlml_event_set_wait")
    ret = fn(st, ctypes.byref(data), timeout)

    check_return(ret)
    return data

def hlmlDeviceGetMACInfo(
        device: hlml_t.HLML_DEVICE.TYPE, count=20, start=0
    ) -> hlml_t.c_hlml_mac_info:
    """ Get MAC addresses of device.
        Count - how many addresses to return
        Start - index to start at
    """
    global _hlmlOBJ
    mac = hlml_t.c_hlml_mac_info()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_mac_info")
    ret = fn(device, ctypes.byref(mac), count, start)

    check_return(ret)
    return mac

def hlmlDeviceERRInject(device: hlml_t.HLML_DEVICE.TYPE, err_type: int) -> None:
    """ Inject error to test response 
        err_type ( 0-endless_cmd / 1-non_fatal / 2-fatal / 3-lose_heartbeat / 4-thermal)
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_device_err_inject")
    ret = fn(device, err_type)

    check_return(ret)
    return None

def hlmlDeviceGetHLRevision(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Returns HL revision """
    global _hlmlOBJ
    rev = ctypes.c_int()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_hl_revision")
    ret = fn(device, ctypes.byref(rev))

    check_return(ret)
    return rev.value

def hlmlDeviceGetPCBInfo(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.c_hlml_pcb_info:
    """ Returns the PCB info """
    global _hlmlOBJ
    pcb = hlml_t.c_hlml_pcb_info()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcb_info")
    ret = fn(device, ctypes.byref(pcb))

    check_return(ret)
    return pcb

def hlmlDeviceGetSerial(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Returns the unique board sn """
    global _hlmlOBJ
    ser = ctypes.create_string_buffer(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_serial")
    ret = fn(device, ctypes.byref(ser))

    check_return(ret)
    return ser

def hlmlDeviceGetBoardID(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the device boardID ( 0 - 7 ) """
    global _hlmlOBJ
    brd = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_board_id")
    ret = fn(device, ctypes.byref(brd))

    check_return(ret)
    return brd.value
    
def hlmlDeviceGetPCIEThroughput(device: hlml_t.HLML_DEVICE.TYPE, counter_type: int) -> int:
    """ Retrieve PCIe utilization information ( over 10ms interval ) 
        counter_type ( 0-TX / 1-RX )
    """
    global _hlmlOBJ
    pcie = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcie_throughput")
    ret = fn(device, counter_type, ctypes.byref(pcie))

    check_return(ret)
    return 

def hlmlDeviceGetPCIEReplayCounter(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the PCIe replay counter """
    global _hlmlOBJ
    pcie = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcie_replay_counter")
    ret = fn(device, ctypes.byref(pcie))

    check_return(ret)
    return pcie.value

def hlmlDeviceGetCurrPCIELinkGeneration(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the current PCIe link generation """
    global _hlmlOBJ
    link = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_curr_pcie_link_generation")
    ret = fn(device, ctypes.c_uint(link))

    check_return(ret)
    return link.value

def hlmlDeviceGetCurrPCIELinkWidth(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the current PCIe link width """
    global _hlmlOBJ
    width = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_curr_pcie_link_width")
    ret = fn(device, ctypes.byref(width))

    check_return(ret)
    return width.value

def hlmlDeviceGetCurrentClocksThrottleReasons(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the current clocks reason for throttling """
    global _hlmlOBJ
    reason = ctypes.c_ulonglong()
    
    fn = _hlmlOBJ.get_func_ptr("hlml_get_current_clocks_throttle_reasons")
    ret = fn(device, ctypes.byref(reason))

    check_return(ret)
    return reason.value

def hlmlDeviceGetTotalEnergyConsumption(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves total energy consumption in mJ since the driver was last reloaded """
    global _hlmlOBJ
    energy = ctypes.c_ulonglong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_total_energy_consumption")
    ret = fn(device, ctypes.byref(energy))

    check_return(ret)
    return energy.value