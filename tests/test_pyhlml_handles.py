import unittest
import os

import pyhlml

def count_from_smi():
	""" Get device count from SMI as a reference """
	with os.popen(
		"/usr/bin/hl-smi --query-aip=name --format=csv,nounits,noheader"
	) as proc:
		stdout = proc.readlines()
	return len(stdout)

def pci_from_smi():
	""" Get PCI bus addresses """
	with os.popen(
		"/usr/bin/hl-smi --query-aip=bus_id --format=csv,nounits,noheader"
	) as proc:
		stdout = proc.readlines()
	for i, line in enumerate(stdout):
		stdout[i] = line.rstrip()
	return stdout

def uuid_from_smi():
	""" Get UUIDs """
	with os.popen(
		"/usr/bin/hl-smi --query-aip=uuid --format=csv,nounits,noheader"
	) as proc:
		stdout = proc.readlines()
	for i, line in enumerate(stdout):
		stdout[i] = line.rstrip()
	return stdout


class TestPyHLML_Handles(unittest.TestCase):
	def setUp(self):
		pyhlml.hlmlInit()

	def tearDown(self):
		pyhlml.hlmlShutdown()

	def test_get_handle_by_index(self):
		""" We expect the number of handles == device count """
		smi_count = count_from_smi()
		devices = []
		for i in range(smi_count):
			device = pyhlml.hlmlDeviceGetHandleByIndex(i)
			self.assertIsNotNone(device.value)
			devices.append(device)
		self.assertEqual(len(devices), smi_count)

	def test_get_handle_by_PCI(self):
		addrs = pci_from_smi()
		devices = []
		for addr in addrs:
			device = pyhlml.hlmlDeviceGetHandleByPCIBusID(addr)
			devices.append(device)
		self.assertEqual(len(devices), len(addrs))
	
	def test_get_handle_by_UUID(self):
		uuids = uuid_from_smi()
		print(uuids)
		devices = []
		for uid in uuids:
			print(uid)
			device = pyhlml.hlmlDeviceGetHandleByPCIBusID(uid)
			devices.append(device)
		self.assertEqual(len(devices), len(uuids))