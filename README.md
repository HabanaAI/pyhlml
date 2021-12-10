# pyhlml
Python3 wrapper for the HLML library

## Getting Started

The pyhlml library is an python API wrapper for the Synapse HLML library, documented here: https://docs.habana.ai/en/latest/API_Reference_Guides/HLML_API_Reference.html

### Requirements

- Python3
- Habana-enabled device ( inc. Drivers/Firmware )
- Synapse version 1.0.1-81 or later

### Install - PIP

```bash
$ pip3 install -e git+https://github.com/HabanaAI/pyhlml.git#egg=pyhlml
```

### Basic Usage

```python3
import pyhlml

# Initialize the library
pyhlml.hlmlInit()

# Get total number of devices in the system
device_count = pyhlml.hlmlDeviceGetCount()

# For each device print utilization
for i in range(device_count):
    device = pyhlml.hlmlDeviceGetHandleByIndex(i)
    print(f"Device {i} Utilization: {pyhlml.hlmlDeviceGetUtilizationRates(device)}

# Shutdown
pyhlml.hlmlShutdown()
```

---

## Versions

This wrapper shadows the synapse release versions and uses the scheme

$release-$build

where release is the synapse release and build is the build of this repo ( 0 indexed ).

### v0.15.0
- Initial Release

### v1.0.1
- Current Release
