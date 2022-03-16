import ctypes

from sys import modules

import pyhlml.hlml_types as hlml_t

from pyhlml.hlml_lib import LibHLML
from pyhlml.hlml_error import HLMLError, ErrorsAsClass

_hlmlOBJ = None

def _wrapperInit():
    """ init module level object and error classes
        Parameters: None
        Returns: None
    """
    ErrorsAsClass()
    setattr(modules[__name__], "_hlmlOBJ", LibHLML())

def check_return(ret):
    """ Checks ret for any error.
        Parameters:
            ret - Symbol for checking if return was valid.
        Returns:
            ret - Symbol for current error status.
    """
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
        Parameters:
            pci_addr (str) - The PCI Address of a habana device.
        Returns:
            device (HLML_DEVICE.TYPE) - The handle for the habana device.
    """
    global _hlmlOBJ

    device = hlml_t.HLML_DEVICE.TYPE
    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_pci_bus_id")
    ret = fn(str.encode(pci_addr), ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetHandleByIndex(index: int) -> hlml_t.HLML_DEVICE.TYPE:
    """ Acquire device handle by index
        Parameters:
            index (int) - The index of a habana device.
        Returns:
            device (HLML_DEVICE.TYPE) - The handle for the habana device.
    """
    global _hlmlOBJ
    device = hlml_t.HLML_DEVICE.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_index")
    ret = fn(index, ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetHandleByUUID(uuid: str) -> hlml_t.HLML_DEVICE.TYPE:
    """ Acquire device handle by UUID
        Parameters:
            uuid (str) - A Universal Unique ID for a habana device to access.
        Returns:
            device (HLML_DEVICE.TYPE) - The handle for the habana device.
    """
    global _hlmlOBJ
    device = hlml_t.HLML_DEVICE.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_handle_by_UUID")
    ret = fn(str.encode(uuid), ctypes.byref(device))

    check_return(ret)
    return device

def hlmlDeviceGetName(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Acquire name of device from handle
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            name (str) - The name of the habana device.
    """
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
    """ Get the PCI attributes of input device
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            pci_info (c_hlml_pci_info) - The PCI attributes of the given device.
    """
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
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            clock_type ( 0-SOC ( GAUDI ) / 1-IC ( GOYA ) / 2-MME ( GOYA ) / 3-TPC ( GOYA ) )
        Returns:
            speed (int) - The clock speed of the selected clock in MHz.
    """
    global _hlmlOBJ
    speed = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_clock_info")
    ret = fn(device, clock_type, ctypes.byref(speed))

    check_return(ret)
    return speed.value

def hlmlDeviceGetMaxClockInfo(device: hlml_t.HLML_DEVICE.TYPE, clock_type=0 ) -> int:
    """ Retrives the maximum speed of the selected clock (MHz)
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            clock_type ( 0-SOC ( GAUDI ) / 1-IC ( GOYA ) / 2-MME ( GOYA ) / 3-TPC ( GOYA ) )
        Returns:
            speed (int) - The MAXIMUM clock speed of the selected clock in MHz.
    """
    global _hlmlOBJ
    speed = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_max_clock_info")
    ret = fn(device, clock_type, ctypes.byref(speed))

    check_return(ret)
    return speed.value

def hlmlDeviceGetUtilizationRates(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Returns utilization over the past second as a percentage
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            hlml_util (int) - The utilization rate over the last second as a percentage.
    """
    global _hlmlOBJ
    hlml_util = hlml_t.c_hlml_utilization()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_utilization_rates")
    ret = fn(device, ctypes.byref(hlml_util))

    check_return(ret)
    return hlml_util.aip

def hlmlDeviceGetMemoryInfo(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.c_hlml_memory:
    """ Returns the total, used, and free memory in bytes
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            hlml_mem (c_hlml_memory) - The total memory and how much is used/free in bytes.
    """
    global _hlmlOBJ
    hlml_mem = hlml_t.c_hlml_memory()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_memory_info")
    ret = fn(device, ctypes.byref(hlml_mem))

    check_return(ret)
    return hlml_mem

def hlmlDeviceGetTemperature(
        device: hlml_t.HLML_DEVICE.TYPE, sensor_type: hlml_t.HLML_TEMP_SENS.TYPE) -> int:
    """ Retrives the current temperature (celsius) of the selected sensor_type
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            sensor_types ( 0-AIP / 1-BOARD )
        Returns:
            temp (int) - The temperature recorded at the given sensor in celsius.
    """
    global _hlmlOBJ
    temp = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_temperature")
    ret = fn(device, sensor_type, ctypes.byref(temp))

    check_return(ret)
    return temp.value

def hlmlDeviceGetTemperatureThreshold(device: hlml_t.HLML_DEVICE.TYPE, threshold_type: int) -> int:
    """ Retrieves the known temperature (celsius) threshold of the requested type
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            threshold_type (0-shutdown / 1-slowdown / 2-memory / 3-gpu ) -  Which threshold temp to check.
        Returns:
            temp (int) - The temperature the given threshold is set at in celsius.
    """
    global _hlmlOBJ
    temp = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_temperature_threshold")
    ret = fn(device, threshold_type, ctypes.byref(temp))

    check_return(ret)
    return temp.value

def hlmlDeviceGetPersistenceMode(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.HLML_ENABLE_STATE:
    """ Retrieves the persistence mode of the device
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            mode (int) - The persistence mode of the device.
    """
    global _hlmlOBJ
    mode = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_persistence_mode")
    ret = fn(device, ctypes.byref(mode))

    check_return(ret)
    return mode.value

def hlmlDeviceGetPerformanceState(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.HLML_P_STATES:
    """ Retrieves the performance state of the device
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            p_state (int) - The performance state of the device.
    """
    global _hlmlOBJ
    p_state = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_performance_state")
    ret = fn(device, ctypes.byref(p_state))

    check_return(ret)
    return p_state.value

def hlmlDeviceGetPowerUsage(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves power usage for the device in mW
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            power (int) - The given device's power usage in mW.
    """
    global _hlmlOBJ
    power = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_power_usage")
    ret = fn(device, ctypes.byref(power))

    check_return(ret)
    return power.value

def hlmlDeviceGetPowerManagementDefaultLimit(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves default power management limit on this device in mW
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            power (int) - The power limit on the device in mW.
    """
    global _hlmlOBJ
    power = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_power_management_default_limit")
    ret = fn(device, ctypes.byref(power))

    check_return(ret)
    return power.value

def hlmlDeviceGetECCMode(device: hlml_t.HLML_DEVICE.TYPE) -> dict:
    """ Retrieves the current and pending ECC modes of the device
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            out (dict) - The current and pending ECC modes for the device.
    """
    global _hlmlOBJ
    out = hlml_t.hlml_ecc_mode()
    current = ctypes.c_uint()
    pending = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_ecc_mode")
    ret = fn(device, ctypes.byref(current), ctypes.byref(pending))

    check_return(ret)
    setattr(out, "current", current)
    setattr(out, "pending", pending)

    return out

def hlmlDeviceGetTotalECCErrors(device: hlml_t.HLML_DEVICE.TYPE, error_type: hlml_t.HLML_MEMORY_ERROR.TYPE, counter_type: hlml_t.HLML_ECC_COUNTER) -> int:
    """ Returns the number of ECC errors for a device. Number is from the last reset, or driver
        reinstall. Currently only the number of corrected errors is supported.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            error_type ( 0-CORRECTED / 1-UNCORRECTED ) - The type of errors to count.
            counter_type ( 0-VOLATILE / 1-AGGREGATE ) - The type of counter to use.
        Returns:
            count (int) - The number of ECC errors for the device, specified by parameters.
    """
    global _hlmlOBJ
    count = ctypes.c_longlong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_total_ecc_errors")
    ret = fn(device, error_type, counter_type, ctypes.byref(count))

    check_return(ret)
    return count.value

def hlmlDeviceGetMemoryErrorCounter(device: hlml_t.HLML_DEVICE.TYPE, error_type: hlml_t.HLML_MEMORY_ERROR.TYPE, counter_type: hlml_t.HLML_ECC_COUNTER.TYPE, location: hlml_t.HLML_MEMORY_LOCATION.TYPE) -> int:
    """ Returns the number of ECC errors for a device at a specified memory location.
        Number is from the last reset, or driver reinstall. Currently only the number
        of corrected errors is supported.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            error_type ( 0-CORRECTED / 1-UNCORRECTED ) - The type of errors to count.
            counter_type ( 0-VOLATILE / 1-AGGREGATE ) - The type of counter to use.
            location ( 0-SRAM / 1-DRAM ) - The type of memory.
        Returns:
            count (int) - The number of ECC errors for the device, specified by parameters.
    """
    global _hlmlOBJ
    ecc_count = ctypes.c_longlong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_memory_error_counter")
    ret = fn(device, error_type, counter_type, location, ctypes.byref(ecc_count))

    check_return(ret)
    return ecc_count.value

def hlmlDeviceGetUUID(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Returns the UUID of the device
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            name (str) - The UUID for the given device.
    """
    global _hlmlOBJ
    name = ctypes.create_string_buffer(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_uuid")
    ret = fn(device, ctypes.byref(name), 256)

    check_return(ret)
    return name.value

def hlmlDeviceGetMinorNumber(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the minor number of the device ( maps to the device node file )
        at /sys/class/habanalabs/hl[minor]
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            number (int) - The minor number for the device.
    """
    global _hlmlOBJ
    number = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_minor_number")
    ret = fn(device, ctypes.byref(number))

    check_return(ret)
    return number.value

def hlmlEventSetCreate() -> hlml_t.HLML_EVENT_SET.TYPE:
    """ Create an empty set of events
        Parameters: None.
        Returns:
            st (HLML_EVENT_SET) - An empty set of events.
    """
    global _hlmlOBJ
    st = hlml_t.HLML_EVENT_SET.TYPE

    fn = _hlmlOBJ.get_func_ptr("hlml_event_set_create")
    ret = fn(ctypes.byref(st))

    check_return(ret)
    return st

def hlmlEventSetFree(st: hlml_t.HLML_EVENT_SET.TYPE) -> None:
    """ Release a set of events
        Parameters:
            st (HLML_EVENT_SET) - The set of events to be released.
        Returns: None.
    """
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
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            event_types ( 0-ECC_err / 1-Crit_err / 2-Clock_change ) - The type of events to start recording.
            st (HLML_EVENT_SET) - The set of events to be released.
        Returns: None.
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
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            timeout (int) - The maximum time to wait for a new event.
        Returns:
            data (c_hlml_event_data) - The data from events ready to be delivered.
    """
    global _hlmlOBJ
    data = hlml_t.c_hlml_event_data()

    fn = _hlmlOBJ.get_func_ptr("hlml_event_set_wait")
    ret = fn(st, ctypes.byref(data), timeout)

    check_return(ret)
    return data

def hlmlDeviceGetMACInfo(
        device: hlml_t.HLML_DEVICE.TYPE, count=20, start=0) -> hlml_t.c_hlml_mac_info:
    """ Get MAC addresses of device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            Count (int) - How many addresses to return.
            Start (int) - The index to start at.
        Returns:
            mac (c_hlml_mac_info) - The MAC addresses of the device.
    """
    global _hlmlOBJ
    mac = hlml_t.c_hlml_mac_info()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_mac_info")
    ret = fn(device, ctypes.byref(mac), count, start)

    check_return(ret)
    return mac

def hlmlDeviceERRInject(device: hlml_t.HLML_DEVICE.TYPE, err_type: int) -> None:
    """ Inject error to test response
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            err_type ( 0-endless_cmd / 1-non_fatal / 2-fatal / 3-lose_heartbeat / 4-thermal) - The type of error to inject.
        Returns: None.
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_device_err_inject")
    ret = fn(device, err_type)

    check_return(ret)
    return None

def hlmlDeviceGetHLRevision(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Returns HL revision
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            rev (int) - The HL revision
    """
    global _hlmlOBJ
    rev = ctypes.c_int()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_hl_revision")
    ret = fn(device, ctypes.byref(rev))

    check_return(ret)
    return rev.value

def hlmlDeviceGetPCBInfo(device: hlml_t.HLML_DEVICE.TYPE) -> hlml_t.c_hlml_pcb_info:
    """ Returns the PCB info
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            pcb (c_hlml_pcb_info) - The info about the device's PCB.
    """
    global _hlmlOBJ
    pcb = hlml_t.c_hlml_pcb_info()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcb_info")
    ret = fn(device, ctypes.byref(pcb))

    check_return(ret)
    return pcb

def hlmlDeviceGetSerial(device: hlml_t.HLML_DEVICE.TYPE) -> str:
    """ Returns the unique board sn
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            ser (str) - The serial number of the device.
    """
    global _hlmlOBJ
    ser = ctypes.create_string_buffer(hlml_t.HLML_DEFINE.HL_FIELD_MAX_SIZE)

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_serial")
    ret = fn(device, ctypes.byref(ser), 256)

    check_return(ret)
    return ser.value

def hlmlDeviceGetBoardID(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the device boardID ( 0 - 7 )
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            brd (int) - The board id of which slot the device is in.
    """
    global _hlmlOBJ
    brd = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_board_id")
    ret = fn(device, ctypes.byref(brd))

    check_return(ret)
    return brd.value

def hlmlDeviceGetPCIEThroughput(device: hlml_t.HLML_DEVICE.TYPE, counter_type: int) -> int:
    """ Retrieve PCIe utilization information ( over 10ms interval )
        counter_type ( 0-TX / 1-RX )
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            counter_type (int) -----------------------------------------------------------------------------
        Returns:
            throughput (int) - The throughput on the PCIE Transfer or Recieve Connection.
    """
    global _hlmlOBJ
    pcie = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcie_throughput")
    ret = fn(device, counter_type, ctypes.byref(pcie))

    check_return(ret)
    return pcie.value

def hlmlDeviceGetPCIEReplayCounter(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the PCIe replay counter
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            pcie (int) - The replay counter of the PCIE device.
    """
    global _hlmlOBJ
    pcie = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_pcie_replay_counter")
    ret = fn(device, ctypes.byref(pcie))

    check_return(ret)
    return pcie.value

def hlmlDeviceGetCurrPCIELinkGeneration(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the current PCIe link generation
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            link (int) - The generation of the device's PCIe link.
    """
    global _hlmlOBJ
    link = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_curr_pcie_link_generation")
    ret = fn(device, ctypes.byref(link))

    check_return(ret)
    return link.value

def hlmlDeviceGetCurrPCIELinkWidth(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieve the current PCIe link width
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            width (int) - The width or lanes of the PCIE connection.
    """
    global _hlmlOBJ
    width = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_curr_pcie_link_width")
    ret = fn(device, ctypes.byref(width))

    check_return(ret)
    return width.value

def hlmlDeviceGetCurrentClocksThrottleReasons(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves the current clocks reason for throttling
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            reason (int) - A code for the reason for the current clock throttle.
    """
    global _hlmlOBJ
    reason = ctypes.c_ulonglong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_current_clocks_throttle_reasons")
    ret = fn(device, ctypes.byref(reason))

    check_return(ret)
    return reason.value

def hlmlDeviceGetTotalEnergyConsumption(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Retrieves total energy consumption in mJ since the driver was last reloaded
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            energy (int) - Total energy consumption of the habana device.
    """
    global _hlmlOBJ
    energy = ctypes.c_ulonglong()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_total_energy_consumption")
    ret = fn(device, ctypes.byref(energy))

    check_return(ret)
    return energy.value

def hlmlDeviceClearCpuAffinity(device: hlml_t.HLML_DEVICE.TYPE) -> None:
    """ Clears a devices Cpu affinity
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            None.
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_device_clear_cpu_affinity")
    ret = fn(device)

    check_return(ret)
    return None

def hlmlDeviceGetCpuAffinity(device: hlml_t.HLML_DEVICE.TYPE, cpu_set_size: int):
    """ Retrieves the CPU affinity set associated with a device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            cpu_set_size - The size of the cpu set.
        Returns:
            cpu_set (int) - The cpu set.
    """
    global _hlmlOBJ
    cpu_set = (ctypes.c_ulong * cpu_set_size)()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_cpu_affinity")
    ret = fn(device, cpu_set_size, ctypes.byref(cpu_set))

    check_return(ret)
    return cpu_set

def hlmlDeviceGetCpuAffinityWithinScope(device: hlml_t.HLML_DEVICE.TYPE, cpu_set_size: int, scope: hlml_t.HLML_AFFINITY_SCOPE.TYPE):
    """ Retrieves the CPU affinity set associated with a device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            cpu_set_size - The size of the cpu set.
            scope - The affinity scope.
        Returns:
            cpu_set (int) - The cpu set.
    """
    global _hlmlOBJ
    cpu_set = (ctypes.c_ulong * cpu_set_size)()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_cpu_affinity_within_scope")
    ret = fn(device, cpu_set_size, ctypes.byref(cpu_set), scope)

    check_return(ret)
    return cpu_set

def hlmlDeviceGetMemoryAffinity(device: hlml_t.HLML_DEVICE.TYPE, node_set_size: int, scope: hlml_t.HLML_AFFINITY_SCOPE.TYPE):
    """ Retrieves the memory affinity set associated with a device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            node_set_size - The size of the node set.
            scope - The affinity scope.
        Returns:
            node_set (int) - The node set.
    """
    global _hlmlOBJ
    node_set = (ctypes.c_ulong * cpu_set_size)()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_memory_affinity")
    ret = fn(device, node_set_size, ctypes.byref(node_set), scope)

    check_return(ret)
    return node_set

def hlmlDeviceSetCpuAffinity(device: hlml_t.HLML_DEVICE.TYPE) -> None:
    """ Sets the CPU affinity with a device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            None.
    """
    global _hlmlOBJ

    fn = _hlmlOBJ.get_func_ptr("hlml_device_set_cpu_affinity")
    ret = fn(device)

    check_return(ret)
    return None

def hlmlDeviceGetViolationStatus(device: hlml_t.HLML_DEVICE.TYPE, perf_policy: hlml_t.HLML_PERF_POLICY.TYPE) -> hlml_t.c_hlml_violation_time:
    """ Gets the violation status of a device.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            perf_policy_type (HLML_PERF_POLICY.TYPE) - The perf policy type (
               0=HLML_PERF_POLICY_POWER 
               1=HLML_PERF_POLICY_THERMAL)
        Returns:
            violation_time (c_hlml_violation_time) - The violation status of the device.
    """
    global _hlmlOBJ

    violation_time = hlml_t.c_hlml_violation_time()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_violation_status")
    ret = fn(device, perf_policy, ctypes.byref(violation_time))

    check_return(ret)
    return violation_time

def hlmlDeviceGetReplacedRowsCount(device: hlml_t.HLML_DEVICE.TYPE, cause: hlml_t.HLML_ROW_REPLACEMENT_CAUSE.TYPE) -> int:
    """ Returns the number of replaced rows.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            cause  (HLML_ROW_REPLACEMENT_CAUSE.TYPE) - The replacement cause to query.
        Returns:
            row_count -> The number of replaced rows
    """
    global _hlmlOBJ

    row_count = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_replaced_rows")
    ret = fn(device, cause, ctypes.byref(row_count), None)

    check_return(ret)
    return row_count.value

def hlmlDeviceGetReplacedRows(device: hlml_t.HLML_DEVICE.TYPE, cause: hlml_t.HLML_ROW_REPLACEMENT_CAUSE.TYPE, row_count: int):
    """ Returns an array of rows replaced by the given cause.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
            cause  (HLML_ROW_REPLACEMENT_CAUSE.TYPE) - The replacement cause to query.
        Returns:
            addresses - An array of hlml_t.c_hlml_row_address structures.
    """
    global _hlmlOBJ

    c_row_count = ctypes.c_uint(row_count)
    addresses = (hlml_t.c_hlml_row_address * row_count)()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_replaced_rows")
    ret = fn(device, cause, ctypes.byref(c_row_count), ctypes.byref(addresses))

    check_return(ret)
    return addresses

def hlmlDeviceGetReplacedRowsPendingStatus(device: hlml_t.HLML_DEVICE.TYPE) -> int:
    """ Returns the pending status of replaced rows.
        Parameters:
            device (HLML_DEVICE.TYPE) - The handle for a habana device.
        Returns:
            is_pending - If there is pending row status.
    """
    global _hlmlOBJ

    is_pending = ctypes.c_uint()

    fn = _hlmlOBJ.get_func_ptr("hlml_device_get_replaced_rows_pending_status")
    ret = fn(device, ctypes.byref(is_pending))

    check_return(ret)
    return is_pending.value
