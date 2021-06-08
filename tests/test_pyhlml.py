import unittest

import pyhlml

class TestPyHLML(unittest.TestCase):
    def setUp(self):
        pyhlml.hlmlInitWithFlags(0)

    def tearDown(self):
        pyhlml.hlmlShutdown()

    def test_init(self):
        pass

    def test_get_device_count(self):
        exp = 4 # Assume HLS1-H
        count = pyhlml.hlmlDeviceGetCount()
        self.assertEqual(count, exp)

    def test_get_handle_by_pci_bus_id(self):
        pci_addr = "000:60:00.0"
        handle = pyhlml.hlmlDeviceGetHandleByPCIBusID(pci_addr)
        print(f"Handle: {handle}")

    def test_get_handle_by_index(self):
        index = 2
        handle = pyhlml.hlmlDeviceGetHandleByIndex(index)
        print(f"Handle: {handle}")

    def test_get_handle_by_uuid(self):
        pass

    def test_device_get_handle_by_uuid(self):
        pass

    def test_device_get_name(self):
        pass

    def test_device_get_pci_info(self):
        pass

    def test_device_get_clock_info(self):
        pass

    def test_device_get_max_clock_info(self):
        pass

    def test_device_get_utilization_rates(self):
        pass

    def test_device_get_memory_info(self):
        pass

    def test_device_get_temperature(self):
        pass

    def test_device_get_temperature_threshold(self):
        pass

    def test_device_get_persistence_mode(self):
        pass

    def test_device_get_performance_state(self):
        pass

    def test_device_get_power_usage(self):
        pass

    def test_device_get_power_management_default_limit(self):
        pass

    def test_device_get_ecc_mode(self):
        pass

    def test_device_get_total_ecc_errors(self):
        pass

    def test_device_get_uuid(self):
        pass

    def test_device_get_minor_number(self):
        pass

    def test_device_register_events(self):
        pass

    def test_event_set_create(self):
        pass

    def test_event_set_free(self):
        pass

    def test_device_get_mac_info(self):
        pass

    def test_device_err_inject(self):
        pass

    def test_device_get_hl_revision(self):
        pass

    def test_device_get_pcb_info(self):
        pass

    def test_device_get_serial(self):
        pass

    def test_device_get_board_id(self):
        pass

    def test_device_get_pcie_throughput(self):
        pass

    def test_device_get_pcie_replay_counter(self):
        pass

    def test_device_get_curr_pcie_link_generation(self):
        pass

    def test_device_get_curr_pcie_link_width(self):
        pass

    def test_device_get_curr_clocks_throttle_reasons(self):
        pass

    def test_device_get_total_energy_consumption(self):
        pass


if __name__ == "__main__":
    unittest.main()