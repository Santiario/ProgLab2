import abc
import PythonLabs.BitLab as btl
import kdprims as kd
import math as m

__author__ = 'Vemund'


class Coder:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def gen_message_from_file(filepath):
        file = open(filepath, 'r')
        message = file.read()
        file.close()

        return message.lower().strip('\n\r')

    @abc.abstractmethod
    def encode(self, string):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def decode(self, bits):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def compression_rate(self, message_length, encoded_length):
        raise NotImplementedError("Please Implement this method")


class AsciiCoder(Coder):
    def encode(self, string):
        result = ''
        for char in string:
            code = bin(ord(char))
            code = code[2:]
            code = '0'*(8-len(code)) + code  # Legger til 0'er foran teksten om den ikke er 8 siffer lang
            result += code
        return result

    def decode(self, bits):
        if len(bits) % 8 != 0:
            raise RuntimeWarning()
        result = ''
        index = 0
        while index < len(bits):
            result += chr(int(bits[index:index+8], 2))
            index += 8
        return result

    def compression_rate(self, message_length, encoded_length):
        return 1 - float(encoded_length)/(8*message_length)

    def encode_decode_test(self, message):
        print('The original message was:\n' + message)
        encoded = self.encode(message)
        print('The encoded message is:\n' + encoded)
        decoded = self.decode(encoded)
        print('The decoded message is:\n' + decoded)
        print()
        print('The length of the original, encoded and decoded message, respectively:\n' +
              str(len(message))+' |', str(len(encoded))+' |', str(len(decoded)))
        if message == decoded:
            print('The message and decoded message match each other.')
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded))*100)+'%')
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')


class HuffmanCoder(Coder):
    def __init__(self):
        self.tree = None
        self.freqs = {}

    def gen_freqs(self, filepath='corpus1.txt'):
        self.freqs = kd.calc_char_freqs(filepath)

    def build_tree(self, freqs):
        pq = btl.init_queue(freqs)
        while len(pq) > 1:
            n1 = pq.pop()
            n2 = pq.pop()
            pq.insert(btl.Node(n1, n2))
        self.tree = pq[0]

    def encode(self, message):
        return btl.huffman_encode(message, self.tree)

    def decode(self, encoded_msg):
        return btl.huffman_decode(encoded_msg, self.tree)

    def compression_rate(self, message_length, encoded_length):
        return 1 - encoded_length/(8.0*message_length)

    def encode_decode_test(self, message):
        print('The original message was:\n' + message)
        encoded = self.encode(message)
        print('The encoded message is:\n' + encoded.__repr__())
        decoded = self.decode(encoded)
        print('The decoded message is:\n' + decoded)
        print()
        print('The length of the original, encoded and decoded message, respectively:\n' +
              str(len(message))+' |', str(len(encoded.__repr__()))+' |', str(len(decoded)))
        if message == decoded:
            print('The message and decoded message match each other.')
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded.__repr__()))*100)+'%')
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')


class LempelZivCoder(Coder):

    def encode(self, bit_string):
        slen = len(bit_string)
        target = bit_string[0]
        lookup_table = {'': 0, bit_string[0]: 1}
        size = 2
        currloc = 1
        while currloc < slen:
            oldseg, newbit = self.find_next_segment(bit_string, currloc, lookup_table)
            bitlen = m.ceil(m.log(size, 2))
            index = lookup_table[oldseg]
            index_bits = self.integer_to_bits(index, bitlen)
            target += (index_bits + newbit)
            lookup_table[oldseg + newbit] = size
            currloc += len(oldseg) + 1
            size += 1
        return target

    @staticmethod
    def find_next_segment(bit_string, loc, table):
        seg = old_seg = ''
        newbit = ''
        while table.get(seg) != None:
            if loc >= len(bit_string):
                return seg, ''
            newbit = bit_string[loc]
            loc += 1
            old_seg = seg
            seg += newbit
        return old_seg, newbit

    @staticmethod
    def integer_to_bits(integer, bitlength):
        bits = str(bin(integer))
        bits = bits[2:]
        bits = '0'*(bitlength-len(bits)) + bits  # Legger til 0'er foran teksten om den ikke er riktig lengde
        return bits

    def decode(self, target):
        tlen = len(target)
        source = target[0]
        lt = ['', target[0]]
        loc = 1
        size = 2
        while loc < tlen:
            bitlen = m.ceil(m.log(size, 2))
            index = int(target[loc: loc + bitlen], 2)
            seg = lt[index]
            if loc + bitlen < tlen:
                seg += target[loc + bitlen]
                size += 1
                lt.append(seg)
                loc += 1
            source += seg
            loc += bitlen
        return source

    def encode_decode_test(self, message):
        print('\nPerforming LZ-compression...')
        print('The original message was:\n' + message)
        encoded = self.encode(message)
        print('The encoded message is:\n' + encoded)
        decoded = self.decode(encoded)
        print('The decoded message is:\n' + decoded)
        print()
        print('The length of the original, encoded and decoded message, respectively:\n' +
              str(len(message))+' |', str(len(encoded))+' |', str(len(decoded)))
        if message == decoded:
            print('The message and decoded message match each other.')
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded))*100)+'%')
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')

    def compression_rate(self, message_length, encoded_length):
        return 1 - float(encoded_length)/message_length


def ascii_test(msg='Hello World', filepath=False, lz_flag=False):
    if filepath:
        msg = Coder.gen_message_from_file(filepath)
    AsciiCoder().encode_decode_test(msg)
    if lz_flag:
        LempelZivCoder().encode_decode_test(AsciiCoder().encode(msg))


def huff_test(msg='Hello World', filepath=False, lz_flag=False):
    msg = msg.lower()
    huffcoder = HuffmanCoder()
    if filepath:
        msg = Coder.gen_message_from_file(filepath)
        huffcoder.gen_freqs(filepath)
    else:
        huffcoder.gen_freqs()
    huffcoder.build_tree(huffcoder.freqs)
    huffcoder.encode_decode_test(msg)
    if lz_flag:
        LempelZivCoder().encode_decode_test(huffcoder.encode(msg).__repr__())


def lz_test(msg='00000000000000000000', filepath=False):
    if filepath:
        msg = Coder.gen_message_from_file(filepath)
    LempelZivCoder().encode_decode_test(msg)


def main():
    #huff_test('sample3.txt', lz_flag=True)
    lz_test(filepath='tumbler_bit.txt')


if __name__ == '__main__':
    main()
