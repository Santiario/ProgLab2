import abc
import PythonLabs.BitLab as btl
import kdprims as kd

__author__ = 'Vemund'


class Coder:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def gen_message_from_file(filepath):
        file = open(filepath, 'r')
        message = file.read()
        file.close()

        return message.lower()

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
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded)))+'%')
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')


class HuffmanCoder(Coder):
    def __init__(self):
        self.tree = None
        self.freqs = {}

    def gen_freqs(self, filepath):
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
        return 1 - float(encoded_length)/message_length

    def encode_decode_test(self, message, filepath):
        self.gen_freqs(filepath)
        self.build_tree(self.freqs)
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
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded.__repr__()))))
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')


if __name__ == '__main__':
    #asciicoder = AsciiCoder()
    #asciicoder.encode_decode_test('Hello world!')

    #print('\n\n-------------------\n\n')

    huffcoder = HuffmanCoder()
    huffcoder.encode_decode_test('110110110110110110101101110101010101010101010101010101010101101111000110101101011010101', 'nullen.txt')
    """
    Dette blir teit. Huffmankoden tar kun for seg enkeltbokstaver, og det er dermed IKKE MULIG aa faa en kortere
    kode enn den originale. Huffman må lete etter ORD, ikke enkelttegn.
    """

