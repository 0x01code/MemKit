import memprocfs
import struct


class memory:
    def __init__(self, process_name) -> None:
        self.vmm = memprocfs.Vmm(['-device', 'fpga'])
        self.process = self.vmm.process(process_name)

    def get_module(self, module_name):
        return self.process.module(module_name)

    def find_chain(self, address, offsets):
        for offset in offsets:
            if self.process.is_wow64:
                address = self.process.memory.read_type(address, 'u64')
            else:
                address = self.process.memory.read_type(address, 'u32')
            address += offset
        return address

    def read(self, address, data_type, max_length=256):
        """
        Valid types: i8, u8, i16, u16, f32, i32, u32, f64, i64, u64, str.
        """
        if data_type == 'str':
            string_bytes = []
            for i in range(max_length):
                byte = self.process.memory.read_type(address + i, 'u8')
                if byte == 0:
                    break
                string_bytes.append(chr(byte))
            return ''.join(string_bytes)
        else:
            return self.process.memory.read_type(address, data_type)

    def write(self, address, data):
        if isinstance(data, str):
            for i in range(16):
                self.process.memory.write(address + i, b'\x00')

            for i, d in enumerate(data):
                self.process.memory.write(address + i, d.encode('utf-8'))
        elif isinstance(data, float):
            return self.process.memory.write(address, struct.pack('f', data))
        else:
            return self.process.memory.write(address, data.to_bytes(data.bit_length() + 7, 'little'))

    def patch(self, dst, src):
        self.process.memory.write(dst, src)

    def nop(self, dst, size):
        nop_array = []
        for _ in range(size):
            nop_array.append(b'\x90')
        self.process.memory.write(dst, b''.join(nop_array))
