# pyhlml
Python3 wrapper for the HLML library

## Getting Started

The pyhlml library is an python API wrapper for the Synapse HLML library, documented here: https://docs.habana.ai/en/latest/API_Reference_Guides/HLML_API_Reference.html

### Requirements

- Python3
- Habana-enabled device ( inc. Drivers/Firmware )
- Synapse version 1.0.1-81 or later

### Install Poetry 
Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

```bash
$ poetry build
Creating virtualenv pyhlml-_6X0icu5-py3.8 in /home/user/.cache/pypoetry/virtualenvs
Building pyhlml (1.0.2)
  - Building sdist
  - Built pyhlml-1.0.2.tar.gz
  - Building wheel
  - Built pyhlml-1.0.2-py3-none-any.whl
```

### Build and Install

#### Build
```bash
$ poetry build
Creating virtualenv pyhlml-_6X0icu5-py3.8 in /home/user/.cache/pypoetry/virtualenvs
Building pyhlml (1.0.2)
  - Building sdist
  - Built pyhlml-1.0.2.tar.gz
  - Building wheel
  - Built pyhlml-1.0.2-py3-none-any.whl
```
After the build packages will be placed in dist directory

#### Install
```bash
$ cd dist
$ pip3 install pyhlml-1.0.2.tar.gz
Defaulting to user installation because normal site-packages is not writeable
Processing ./pyhlml-1.0.2.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: setuptools>=42 in /usr/lib/python3/dist-packages (from pyhlml==1.0.2) (45.2.0)
Requirement already satisfied: wheel<0.38.0,>=0.37.0 in /usr/local/lib/python3.8/dist-packages (from pyhlml==1.0.2) (0.37.0)
Building wheels for collected packages: pyhlml
  Building wheel for pyhlml (pyproject.toml) ... done
  Created wheel for pyhlml: filename=pyhlml-1.0.2-py3-none-any.whl size=9934 sha256=5539825e857d6ae0208cf47aa6a885f077ed7720607fdd24f8804ae6f2586ad0
  Stored in directory: /home/ubuntu/.cache/pip/wheels/c8/c0/cc/c7da74c7afffa9f794b952092baf2fd0b8a4e962e2537c3d35
Successfully built pyhlml
Installing collected packages: pyhlml
Successfully installed pyhlml-1.0.2
```

#### Verify
```bash
$ pip3 show pyhlml
Name: pyhlml
Version: 1.0.2
Summary: Python3 wrapper for the HLML library.
Home-page:
Author: Keegan van Gemeren
Author-email: kvangemeren@habana.ai
License: UNKNOWN
Location: /home/ubuntu/.local/lib/python3.8/site-packages
Requires: setuptools, wheel
Required-by:
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

### v1.0.2
- Current Release
