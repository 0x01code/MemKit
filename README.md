# Memkit
Memkit is an game hacking library for Direct Memory Access (DMA) 

# Example
```
from memkit import Memory

mem = Memory('ac_client.exe')
module = mem.GetModule('ac_client.exe')

health_address = mem.FindChain(module.base + 0x0018AC00, [0xEC])

mem.Write(health_address, 1337)

health = mem.Read(health_address, 'i32')
```