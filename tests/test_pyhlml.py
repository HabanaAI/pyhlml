from pyhlml.main import hlmlDeviceGetPCIEThroughput
import unittest

import pyhlml

_hlmlOBJ = pyhlml.libhlml.LibHLML()

class TestPyHLML(unittest.TestCase):

    def setUp(self):
        global _hlmlOBJ
        if _hlmlOBJ.ref_count == 0:        
            pyhlml.hlmlInitWithFlags(0)

    def tearDown(self):
        pyhlml.hlmlShutdown()

    def test_init(self):
        pass

    def test_get_device_count(self):
        count = pyhlml.hlmlDeviceGetCount()
        self.assertEqual(count, 4) # Assume HLS1-H

    def test_get_handle_by_pci_bus_id(self):
        pci_addr = "000:60:00.0"
        handle = pyhlml.hlmlDeviceGetHandleByPCIBusID(pci_addr)
        self.assertNotEqual(handle, None)

    def test_get_handle_by_index(self):
        index = 2
        handle = pyhlml.hlmlDeviceGetHandleByIndex(index)
        self.assertNotEqual(handle, None)

    def test_device_get_handle_by_uuid(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        uuid = pyhlml.hlmlDeviceGetUUID(device)
        u_device = pyhlml.hlmlDeviceGetHandleByUUID(uuid)
        print(f"\n{device} / {u_device}")
        self.assertEqual(device, u_device)

    def test_device_get_name(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        name = pyhlml.hlmlDeviceGetName(device)
        print(f"\nName: {name}")

    def test_device_get_pci_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        pci_info = pyhlml.hlmlDeviceGetPCIInfo(device)
        print(f"\nPCI Info: {pci_info}")

    def test_device_get_clock_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        clock_speed = pyhlml.hlmlDeviceGetClockInfo(device, 0)
        print(f"\nSOC Clock: {clock_speed}")

    def test_device_get_max_clock_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        max_clock = pyhlml.hlmlDeviceGetMaxClockInfo(device, 0)
        print(f"\nMAX SOC Clock: {max_clock}")

    def test_device_get_utilization_rates(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        util_rates = pyhlml.hlmlDeviceGetUtilizationRates(device)
        print(f"\nUTIL: {util_rates}")

    def test_device_get_memory_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        mem_info = pyhlml.hlmlDeviceGetMemoryInfo(device)
        print(f"\nMEM INFO: {mem_info}")

    def test_device_get_temperature(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        a_temp = pyhlml.hlmlDeviceGetTemperature(device, 0)
        b_temp = pyhlml.hlmlDeviceGetTemperature(device, 1)
        print(f"\nAIP TEMP: {a_temp}")
        print(f"BOARD TEMP: {b_temp}")

    def test_device_get_temperature_threshold(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"\nShutdown Temp Thresh: {pyhlml.hlmlDeviceGetTemperatureThreshold(device, 0)}")
        print(f"Slowdown Temp Thresh: {pyhlml.hlmlDeviceGetTemperatureThreshold(device, 1)}")
        print(f"Memory Temp Thresh: {pyhlml.hlmlDeviceGetTemperatureThreshold(device, 2)}")
        print(f"GPU Temp Thresh: {pyhlml.hlmlDeviceGetTemperatureThreshold(device, 3)}")

    def test_device_get_power_usage(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"\nPower Usage: {pyhlml.hlmlDeviceGetPowerUsage(device)}")

    def test_device_get_power_management_default_limit(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"\nPower Limit: {pyhlml.hlmlDeviceGetPowerManagementDefaultLimit(device)}")

    def test_device_get_ecc_mode(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        result = pyhlml.hlmlDeviceGetECCMode(device)
        print(f"\nCurrent: {result['current']}\nPending: {result['pending']}")

    def test_device_get_total_ecc_errors(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"\nVolatile_err: {pyhlml.hlmlDeviceGetTotalECCErrors(device, 0, 0)}")
        print(f"Aggregate_err: {pyhlml.hlmlDeviceGetTotalECCErrors(device, 0, 1)}")

    def test_device_get_uuid(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"\nUUID: {pyhlml.hlmlDeviceGetUUID(device)}")

    def test_device_get_minor_number(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"Minor: {pyhlml.hlmlDeviceGetMinorNumber(device)}")

    def test_device_get_mac_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"MAC: {pyhlml.hlmlDeviceGetMACInfo(device)}")

    def test_device_get_hl_revision(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"HL-Rev: {pyhlml.hlmlDeviceGetHLRevision(device)}")

    def test_device_get_pcb_info(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"PCB INFO: {pyhlml.hlmlDeviceGetPCBInfo(device)}")

    def test_device_get_serial(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"SN: {pyhlml.hlmlDeviceGetSerial(device)}")

    def test_device_get_board_id(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"BRD ID: {pyhlml.hlmlDeviceGetBoardID(device)}")

    def test_device_get_pcie_throughput(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"TX THRU: {hlmlDeviceGetPCIEThroughput(device, 0)}")
        print(f"RX THRU: {hlmlDeviceGetPCIEThroughput(device, 1)}")

    def test_device_get_pcie_replay_counter(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"PCIE Replay: {pyhlml.hlmlDeviceGetPCIEReplayCounter(device)}")

    def test_device_get_curr_pcie_link_generation(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"PCIE Link Gen: {pyhlml.hlmlDeviceGetCurrPCIELinkGeneration(device)}")

    def test_device_get_curr_pcie_link_width(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"PCIE Link Width: {pyhlml.hlmlDeviceGetCurrPCIELinkWidth(device)}")

    def test_device_get_curr_clocks_throttle_reasons(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0)
        print(f"Throttle Reason: {pyhlml.hlmlDeviceGetCurrentClocksThrottleReasons(device)}")

    def test_device_get_total_energy_consumption(self):
        device = pyhlml.hlmlDeviceGetHandleByIndex(0) 
        print(f"{pyhlml.hlmlDeviceGetTotalEnergyConsumption(device)}")

if __name__ == "__main__":
    unittest.main()