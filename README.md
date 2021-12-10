# pyhlml
Python3 wrapper for the HLML library

## Getting Started

In the future you will be able to install this library with pip.

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
