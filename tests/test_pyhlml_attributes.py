import unittest
import pprint

import pyhlml

def count_from_smi():
        """ Get device count from SMI as a reference """
        with os.popen(
                "/usr/bin/hl-smi --query-aip=name --format=csv,nounits,noheader"
        ) as proc:
                stdout = proc.readlines()
        return len(stdout)

class TestPyHLML_Attributes(unittest.TestCase):
    def setUp(self):
        pyhlml.hlmlInit()
        self.device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        
    def tearDown(self):
        pyhlml.hlmlShutdown()
    
    def test_Attributes(self):
        for method, attr in self.getAttributes():
            try:
                attr()
            except Exception as e:
                print(f"Uh-oh in {method}")
        pp = pprint.PrettyPrinter(indent=4)
        output = {
            "Index": 0,
            "Name": self.name,
            "PCI Info": {
                "Bus": self.pci_info.bus,
                "Bus_id": self.pci_info.bus_id,
                "Device": self.pci_info.device,
                "Domain": self.pci_info.domain,
                "PCI_device_id": self.pci_info.pci_device_id,
                "caps": {
                    "link_speed": self.pci_info.caps.link_speed,
                    "link_width": self.pci_info.caps.link_width
                }
            },
            "Max Clock": self.max,
            "Temp Thresholds": {
                "Shutdown": self.shutdown_tmp_thrsh,
                "Slowdown": self.slowdown_tmp_thrsh,
                "Memory": self.mem_tmp_thrsh,
                "GPU": self.gpu_tmp_thrsh
            },
            #"Power Management Limit": self.power_default_limit,
            "ECC_Mode": {
                "Current": self.current_ecc_mode,
                "Pending": self.pending_ecc_mode
            },
            "UUID": self.uuid,
            "Minor": self.minor_number,
            "MAC Info": self.mac_info,
            "Serial": self.serial,
            "PCB Info": self.pcb_info,
            "PCB Info": {
                "PCB_VER": self.pcb_info.pcb_ver,
                "PCB_ASSEMBLY_VER": self.pcb_info.pcb_assembly_ver
            },
            "HL REV": self.hl_rev,
            "BRD ID": self.brd_id
        }

        pp.pprint(output)

    def getAttributes(self):
        for method in dir(self):
            if method.startswith("get_"):
                yield method, getattr(self, method)

    def get_name(self):
        self.name = pyhlml.hlmlDeviceGetName(self.device)
        self.assertIsNotNone(self.name)

    def get_pci_info(self):
        self.pci_info = pyhlml.hlmlDeviceGetPCIInfo(self.device)
        self.assertIsNotNone(self.pci_info)  

    def get_max_clock_info(self):
        self.max = pyhlml.hlmlDeviceGetMaxClockInfo(self.device)
        self.assertIsNotNone(self.max)

    def get_temp_threshold(self):
        self.shutdown_tmp_thrsh = pyhlml.hlmlDeviceGetTemperatureThreshold(self.device, 0)
        self.slowdown_tmp_thrsh = pyhlml.hlmlDeviceGetTemperatureThreshold(self.device, 1)
        self.mem_tmp_thrsh = pyhlml.hlmlDeviceGetTemperatureThreshold(self.device, 2)
        self.gpu_tmp_thrsh = pyhlml.hlmlDeviceGetTemperatureThreshold(self.device, 3)
        self.tmp_thrshs = [
            self.shutdown_tmp_thrsh,
            self.slowdown_tmp_thrsh,
            self.mem_tmp_thrsh,
            self.gpu_tmp_thrsh
        ]

        for thrsh in self.tmp_thrshs:
            self.assertIsNotNone(thrsh)

    def get_power_management_default_limit(self):
        self.power_default_limit = pyhlml.hlmlDeviceGetPowerManagementDefaultLimit(self.device)
        self.assertIsNotNone(self.power_default_limit)

    def get_ecc_mode(self):
        res = pyhlml.hlmlDeviceGetECCMode(self.device)
        self.current_ecc_mode = res['current']
        self.pending_ecc_mode = res['pending']
        self.assertIsNotNone(self.current_ecc_mode)
        self.assertIsNotNone(self.pending_ecc_mode)

    def get_uuid(self):
        self.uuid = pyhlml.hlmlDeviceGetUUID(self.device)
        self.assertIsNotNone(self.uuid)

    def get_minor_number(self):
        self.minor_number = pyhlml.hlmlDeviceGetMinorNumber(self.device)
        self.assertIsNotNone(self.minor_number)

    def get_mac_info(self):
        self.mac_info = pyhlml.hlmlDeviceGetMACInfo(self.device)
        self.assertIsNotNone(self.mac_info)

    def get_serial(self):
        self.serial = pyhlml.hlmlDeviceGetSerial(self.device)
        self.assertIsNotNone(self.serial)

    def get_pcb_info(self):
        self.pcb_info = pyhlml.hlmlDeviceGetPCBInfo(self.device)
        self.assertIsNotNone(self.pcb_info)

    def get_hl_rev(self):
        self.hl_rev = pyhlml.hlmlDeviceGetHLRevision(self.device)
        self.assertIsNotNone(self.hl_rev)

    def get_brd_id(self):
        self.brd_id = pyhlml.hlmlDeviceGetBoardID(self.device)
        self.assertIsNotNone(self.brd_id)

if __name__ == "__main__":
    unittest.main()