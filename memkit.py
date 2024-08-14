import memprocfs
import struct


class Memory:
    def __init__(self, process_name) -> None:
        self.vmm = memprocfs.Vmm(['-device', 'fpga'])
        self.process = self.vmm.process(process_name)

    def GetModule(self, module_name):
        return self.process.module(module_name)

    def FindChain(self, address, offsets):
        for offset in offsets:
            # Haven't checked how many bits it is yet.
            address = self.process.memory.read_type(address, 'u32')
            address += offset
        return address

    # Valid types: i8, u8, i16, u16, f32, i32, u32, f64, i64, u64.
    def Read(self, address, data_type):
        return self.process.memory.read_type(address, data_type)

    def Write(self, address, data):
        if isinstance(data, str):
            for i in range(16):
                self.process.memory.write(address + i, b'\x00')

            for i, d in enumerate(data):
                self.process.memory.write(address + i, d.encode('utf-8'))
        elif isinstance(data, float):
            return self.process.memory.write(address, struct.pack('f', data))
        else:
            return self.process.memory.write(address, data.to_bytes(data.bit_length() + 7, 'little'))
