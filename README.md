# Memkit
Memkit is game hacking library for Direct Memory Access (DMA) 

# Example
```python
from memkit import Memory

mem = Memory('ac_client.exe')
module = mem.get_module('ac_client.exe')

health_address = mem.find_chain(module.base + 0x0018AC00, [0xEC])

mem.write(health_address, 1337)

health = mem.read(health_address, 'i32')
```
