import memprocfs
import re
import struct
from keystone import *


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

    def pattern_scan(self, module, pattern):
        memory = self.process.memory.read(module.base, module.image_size)

        regex_pattern = pattern.replace(' ', '').replace('??', '.')
        regex_pattern = re.sub(r'([0-9A-Fa-f]{2})', r'\\x\1', regex_pattern)
        regex = re.compile(regex_pattern.encode())

        match = regex.search(memory)

        if match:
            return module.base + match.start()
        else:
            return None

    def alloc(self):
        # Not yet usable, need to learn more.
        for v in self.process.maps.vad():
            if v['protection'] == '--rw--':
                return v['start']

    def hook(self, address, data, length):
        '''
        Example: mem.hook(0x400000, code = 'inc dword ptr [eax]\nlea eax, dword ptr [esp + 0x1C]', 6)
        '''
        if length < 5:
            return False

        self.nop(address, length)

        target_address = self.alloc()
        jump_offset = target_address - (address + 5)
        hook_code = b'\xE9' + struct.pack('<i', jump_offset)
        self.patch(address, hook_code)

        # Convert asm code to bytes
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        encoding, _ = ks.asm(data)
        hook_code = bytes.fromhex(''.join(format(x, "02x") for x in encoding))

        # jump back to original address
        jump_back_address = address + length
        jump_offset = jump_back_address - (target_address + len(hook_code) + 5)
        hook_code += b'\xE9' + struct.pack('<i', jump_offset)

        self.patch(target_address, hook_code)
