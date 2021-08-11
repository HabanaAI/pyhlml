import unittest
import pprint
import os

import pyhlml

class TestPyHLML_Metrics(unittest.TestCase):
    def setUp(self):
        pyhlml.hlmlInit()
        self.device = pyhlml.hlmlDeviceGetHandleByIndex(0)
	
    def tearDown(self):
        pyhlml.hlmlShutdown()

    def getMetrics(self):
        for method in dir(self):
            if method.startswith("get_"):
                yield method, getattr(self, method)

    def test_metrics(self):
        for method, attr in self.getMetrics():
            try:
                attr()
            except:
                print(f"Failure in {method}")
        pp = pprint.PrettyPrinter(indent=4)
        output = {
            "Device Count": self.m_count,
            "Clock Info": self.clock_info,
            "Util Rate": self.util,
            "Memory": {
                "Free": self.mem_stat.free,
                "Used": self.mem_stat.used,
                "Total": self.mem_stat.total
            },
            "Current Temps": {
                "Board": self.brd_tmp,
                "AIP": self.aip_tmp
            },
            "Power Usage": self.pow_usg,
            "Total ECC Errors": {
                "Volatile": self.err_corr_vol,
                "Aggregate": self.err_corr_agg
            },
            "PCIE Throughput": {
                "TX": self.pci_tx,
                "RX": self.pci_rx
            },
            "PCIE Replays": self.pcie_replay,
            #"PCIE_LINK_GEN": self.pcie_link_gen,
            "PCIE_LINK_WIDTH": self.pcie_link_width,
            "Throttle Reasons": self.throttle_reason,
            "Power Consumption": self.consumption
        }
        print("")
        pp.pprint(output)

    def get_device_count(self):
        self.m_count = pyhlml.hlmlDeviceGetCount()
        self.assertIsNotNone(self.m_count)

    def get_clock_info(self):
        self.clock_info = pyhlml.hlmlDeviceGetClockInfo(self.device)
        self.assertIsNotNone(self.clock_info)
    
    def get_utilization_rates(self):
        self.util = pyhlml.hlmlDeviceGetUtilizationRates(self.device)
        self.assertIsNotNone(self.get_utilization_rates)
   
    def get_memory_info(self):
        self.mem_stat = pyhlml.hlmlDeviceGetMemoryInfo(self.device)
        self.assertIsNotNone(self.mem_stat)

    def get_temperature(self):
        self.aip_tmp = pyhlml.hlmlDeviceGetTemperature(self.device, 0)
        self.brd_tmp = pyhlml.hlmlDeviceGetTemperature(self.device, 1)
        self.assertIsNotNone(self.aip_tmp)
        self.assertIsNotNone(self.brd_tmp)

    def get_power_usage(self):
        self.pow_usg = pyhlml.hlmlDeviceGetPowerUsage(self.device)
        self.assertIsNotNone(self.pow_usg)

    def get_total_ecc_errors(self):
        self.err_corr_vol = pyhlml.hlmlDeviceGetTotalECCErrors(self.device, 0, 0)
        self.err_corr_agg = pyhlml.hlmlDeviceGetTotalECCErrors(self.device, 0, 1)
        self.assertIsNotNone(self.err_corr_agg)
        self.assertIsNotNone(self.err_corr_agg)

    def get_pcie_throughput(self):
        self.pci_tx = pyhlml.hlmlDeviceGetPCIEThroughput(self.device, 0)
        self.pci_rx = pyhlml.hlmlDeviceGetPCIEThroughput(self.device, 1)
        self.assertIsNotNone(self.pci_tx)
        self.assertIsNotNone(self.pci_rx)

    def get_pcie_replay_counter(self):
        self.pcie_replay = pyhlml.hlmlDeviceGetPCIEReplayCounter(self.device)
        self.assertIsNotNone(self.pcie_replay)

    def get_pcie_link_gen(self):
        self.pcie_link_gen = pyhlml.hlmlDeviceGetCurrPCIELinkGeneration(self.device)
        self.assertIsNotNone(self.pcie_link_gen)

    def get_pcie_link_width(self):
        self.pcie_link_width = pyhlml.hlmlDeviceGetCurrPCIELinkWidth(self.device)
        self.assertIsNotNone(self.pcie_link_width)

    def get_clock_throttle_reasons(self):
        self.throttle_reason = pyhlml.hlmlDeviceGetCurrentClocksThrottleReasons(self.device)
        self.assertIsNotNone(self.throttle_reason)

    def get_total_consumption(self):
        self.consumption = pyhlml.hlmlDeviceGetTotalEnergyConsumption(self.device)
        self.assertIsNotNone(self.consumption)
       
if __name__ == "__main__":
    unittest.main()