# Memkit
[![release](https://img.shields.io/github/release/0x01code/memkit.svg)](https://github.com/0x01code/MemKit/releases)
[![version](https://img.shields.io/pypi/v/memkit.svg)](https://pypi.org/project/memkit)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/memkit)


Memkit is game hacking library for Direct Memory Access (DMA) 

A detailed usage guide is available on [Docs](https://github.com/0x01code/MemKit/wiki/Docs) section of the Wiki.

# Feature
- Get module address
- Find chain
- Read memory
- Write memory
- Patch binary
- Nop binary
- Pattern scan

# Install
You can install memkit with pip as following:
```
pip install memkit
```

# Example
```python
from memkit import memory

mem = memory('ac_client.exe')
module = mem.get_module('ac_client.exe')

health_address = mem.find_chain(module.base + 0x0018AC00, [0xEC])

mem.write(health_address, 1337)

health = mem.read(health_address, 'i32')
```
