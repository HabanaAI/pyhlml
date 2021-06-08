"""
Python bindings for HLML types
"""

import ctypes

class HLML_DEFINE:
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

class _PrintS(ctypes.Structure):
    """
    Produces nicer __str__ output than ctypes.Structure.
    
    e.g. instead of:
      
    > print str(obj)
    <class_name object at 0x7fdf82fef9e0>
    
    this class will print...

    > print str(obj)
    class_name(field_name: formatted_value, field_name: formatted_value)
    _fmt_ dictionary of <str _field_ name> -> <str format>
    
    Default formatting string for all fields can be set with key "<default>" like:
      _fmt_ = {"<default>" : "%d MHz"} # e.g all values are numbers in MHz.

    If not set it's assumed to be just "%s"

    e.g. class that has _field_ 'hex_value', c_uint could be formatted with
      _fmt_ = {"hex_value" : "%08X"}
    to produce nicer output.
    """
    _fmt_ = {}
    def __str__(self):
        result = []
        for x in self._fields_:
            key = x[0]
            value = getattr(self, key)
            fmt = "%s"
            if key in self._fmt_:
                fmt = self._fmt_[key]
            elif "<default>" in self._fmt_:
                fmt = self._fmt_["<default>"]
            result.append(("%s: " + fmt) % (key, value))
        return self.__class__.__name__ + "(" +  ", ".join(result) + ")"

class c_hlml_pci_cap(_PrintS):
    _fields_ = [("link_speed", ctypes.c_char * HLML_DEFINE.PCI_LINK_INFO_LEN),
                ("link_width",ctypes.c_char * HLML_DEFINE.PCI_LINK_INFO_LEN)
               ]

class c_hlml_pci_info(_PrintS):
    """
    /*
        * bus - The bus on which the device resides, 0 to 0xf
        * bus_id - The tuple domain:bus:device.function
        * device - The device's id on the bus, 0 to 31
        * domain - The PCI domain on which the device's bus resides
        * pci_device_id - The combined 16b deviceId and 16b vendor id
    */
    """
    _fields_ = [("bus", ctypes.c_uint),
                ("bus_id", ctypes.c_char * HLML_DEFINE.PCI_ADDR_LEN),
                ("device", ctypes.c_uint),
                ("domain", ctypes.c_uint),
                ("pci_device_id", ctypes.c_uint),
                ("caps", c_hlml_pci_cap)
               ]

class c_hlml_utilization(_PrintS):
    _fields_ = [("aip", ctypes.c_uint)]

class c_hlml_memory(_PrintS):
    _fields_ = [("free", ctypes.c_ulonglong),
                ("total", ctypes.c_ulonglong),
                ("used", ctypes.c_ulonglong)
               ]

class c_hlml_pcb_info(_PrintS):
    _fields_ = [("pcb_ver", ctypes.c_char * HLML_DEFINE.HL_FIELD_MAX_SIZE),
                ("pcb_assembly_ver", ctypes.c_char * HLML_DEFINE.HL_FIELD_MAX_SIZE)
               ]

class c_hlml_event_data(_PrintS):
    _fields_ = [("device", ctypes.c_void_p),
                ("event_type", ctypes.c_ulonglong)
               ]

class c_hlml_mac_info(_PrintS):
    _fields_ = [("addr", ctypes.c_ubyte * HLML_DEFINE.ETHER_ADDR_LEN), # unsigned char
                ("id", ctypes.c_int)
               ]

"""
Helpers
"""

## Alternative object
# Allows the object to be printed
# Allows mismatched types to be assigned
#  - like None when the Structure variant requires c_uint

class hlml_friendly_obj(object):
    def __init__(self, dic):
        for x in dic:
            setattr(self, x, dic[x])
    def __str__(self):
        return self.__dict__.__str__()

def hlml_struct_to_friendly(struct):
    dic = {}
    for x in struct._fields_:
        key = x[0]
        value = getattr(struct, key)
        dic[key] = value
    obj = hlml_friendly_obj(dic)
    return obj

def hlml_friendly_to_struct(obj, model):
    for x in model._fields_:
        key = x[0]
        value = obj.__dict__[key]
        setattr(model, key, value)
    return model